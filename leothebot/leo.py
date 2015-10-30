#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Leo's brains, coupled to Telegram's data model
# author: tony@lazarew.me


import random

from twisted.internet import reactor, defer

from quotes import QuoteFetcher
from state import state as singleton_state


# NLTK stuff, will move out
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer


def reactor_sleep(sleep_time):
    """Reactor based sleep()."""
    d = defer.Deferred()
    reactor.callLater(sleep_time, d.callback, None)
    return d


class Leo(object):
    def __init__(self, telegram, state=None, quotes=None, translate=None):
        self.telegram = telegram

        if quotes is None:
            quotes = QuoteFetcher()
        self.quotes = quotes

        if state is None:
            state = singleton_state
        self.state = state

        self.translate = translate

        self._config = self.state.config['leo_brain']

        # NLTK stuff
        self.nl_init_stemmer(self._config.setdefault('nltk_language', 'english'))
        self.state.runtime['address_stems'] = \
            self.nl_extract_stems(self._config.setdefault('addresses', []))

    #
    # TODO(tony): This will move out to a separate language processing
    # class. For now it's just a PoC and stays here.
    #

    def nl_init_stemmer(self, language):
        self.stemmer = SnowballStemmer(language)

    def nl_stem(self, word):
        return self.stemmer.stem(word)

    def nl_extract_stems(self, words):
        stems = set()
        for word in words:
            stems.add(self.nl_stem(word).encode('utf8'))
        return stems

    def nl_find_address_in_text(self, text, language='english'):
        allowed_punct = ('.', '!', '?', ',')
        found = False

        for sentence in sent_tokenize(text, language=language):
            if found:
                break

            for word in word_tokenize(sentence, language=language):
                stem = self.stemmer.stem(word).encode('utf8')
                if stem in self.state.runtime['address_stems']:
                    found = True
                    continue

                if found:
                    if word[0] in allowed_punct:
                        break
                    else:
                        found = False

        if found:
            return True

        return False

    #
    # State persistence between service restarts
    #

    def restore_state(self):
        pass

    def persist_state(self):
        pass

    #
    # Incoming triggers processing
    #

    def reaction_delay(self, payload):
        """Realistic incoming messages reaction delay.

        TODO(tony): definitely depending on which chat we got the message in
        and probably depending on who sent it.
        """
        return reactor_sleep(random.randint(2, 6))

    def incoming_message(self, payload):
        """This is being triggered by the transport whenever we receive a new
        message.
        """
        print("payload=%r" % payload)

        # Process the incoming message
        d_process = self.process_message(payload)

        # Possibly respond to a message
        d_respond = self.respond_with_something(payload)

        return defer.DeferredList([d_process, d_respond])

    @defer.inlineCallbacks
    def respond_with_something(self, payload):
        should_respond = yield self.should_respond(payload)
        if not should_respond:
            defer.returnValue(None)

        text = payload['message']['text']
        chat_id = payload['message']['chat']['id']
        reply_to_message_id = random.choice(
            (None, payload['message']['message_id']))

        respond_with_quote = random.choice([False, True])
        double_translate = random.choice([False, True])

        if respond_with_quote:
            reponse_text = yield self.quotes.get_quote()
        else:
            reponse_text = text
            double_translate = True

        if double_translate:
            reponse_text = yield self.double_translate(reponse_text)

        print("respond_with_quote = %r" % respond_with_quote)
        print("double_translate = %r" % double_translate)

        yield self.send_message(
            chat_id=chat_id,
            text=reponse_text,
            reply_to_message_id=reply_to_message_id)

    @defer.inlineCallbacks
    def should_respond(self, payload):
        # Check if the bot should respond to an event
        if 'text' not in payload['message']:
            defer.returnValue(False)

        # Simulating reaction
        yield self.reaction_delay(payload)

        # Respond if the message is a direct reply to one of the bot's messages
        bot_name = self._config['telegram_bot_name']
        try:
            if bot_name == payload['message']['reply_to_message']['from']['username']:
                print("should_respond(): yes, direct reply")
                defer.returnValue(True)
        except KeyError:
            pass

        # Check if the message is addressed to the bot
        if self.nl_find_address_in_text(payload['message']['text']):
            print("should_respond(): yes, was mentioned")
            defer.returnValue(True)

        defer.returnValue(False)

    @defer.inlineCallbacks
    def double_translate(self, text):
        # This is a simple Google translate trick. This method will eventually
        # become saner.
        detection = yield self.translate.detect(text=text)
        src_lang = detection['data']['detections'][0][0]['language']
        print("src_lang = %r" % src_lang)

        languages = yield self.translate.languages()
        dest_lang = random.choice([l for l in languages.keys() if l != src_lang])
        print("dest_lang = %r" % dest_lang)

        # Translate forth and back
        translation = yield self.translate.translate(
            text=text, source=src_lang, target=dest_lang)
        dest_text = translation['data']['translations'][0]['translatedText']

        translation = yield self.translate.translate(
            text=dest_text,
            source=dest_lang,
            target=self._config['google_translate_language'])
        defer.returnValue(translation['data']['translations'][0]['translatedText'])

    #
    # Output methods with realistic chat actions
    #

    @defer.inlineCallbacks
    def send_message(self, chat_id, text, **kw):
        # Simulate typing
        typing_delay = int(self._config['typing_speed'] * len(text))
        print('typing for %d sec' % typing_delay)

        # After a while chat action does expire. This loop makes sure
        # that it is being updated regularly.
        for i in range(0, typing_delay + 1, 3):
            yield self.telegram.send_chat_action(
                chat_id=chat_id,
                action='typing')

            iteration_time = 3 if typing_delay - i >= 3 else typing_delay - i

            yield reactor_sleep(iteration_time)

            # Simulate pauses humans do while typing (to think?)
            if random.randint(1, 10) == 1:
                yield reactor_sleep(10)

        yield self.telegram.send_message(chat_id=chat_id, text=text, **kw)

    #
    # Text processing
    #
    def process_message(self, payload):
        # TODO(tony): parse the message, analyze it, log it, whatever needed
        return defer.succeed(True)
