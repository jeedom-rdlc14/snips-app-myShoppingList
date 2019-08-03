#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
import logging

CONFIG_INI = "config.ini"
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

lang = "FR"

logging.basicConfig(format='%(asctime)s [%(threadName)s] - [%(levelname)s] - %(message)s', level=logging.INFO,
                    filename='shoppingList.log', filemode='w'
                    )

logger = logging.getLogger('myQuitchen')
logger.addHandler(logging.StreamHandler())

class ShoppingList(object):
    """
    Class used to wrap action code with mqtt connection
    """

    def __init__(self):
        # get the configuration if needed
        #try:
        #    self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        #except :
        #    self.config = None

        # start listening to MQTT
        self.start_blocking()

    # --> Sub callback function, one per intent
    def intent_add_callback(self, hermes, intent_message):
        logger.info('...intent-add...')
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))

        # if need to speak the execution result by tts
        #hermes.publish_start_session_notification(intent_message.site_id, "Action1 has been done")

    def intent_delete_callback(self, hermes, intent_message):
        logger.info('...intent-delete...')
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))

        # if need to speak the execution result by tts
        # hermes.publish_start_session_notification(intent_message.site_id,"Action2 has been done")

    def intent_list_callback(self, hermes, intent_message):
        logger.info('...intent-list...')
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))

        # if need to speak the execution result by tts
        #hermes.publish_start_session_notification(intent_message.site_id,"Action2 has been done")

    def intent_flush_callback(self, hermes, intent_message):
        logger.info('...intent-flush...')
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))

        # if need to speak the execution result by tts
        #hermes.publish_start_session_notification(intent_message.site_id,"Action2 has been done")

    def intent_print_callback(self, hermes, intent_message):
        logger.info('...intent-print...')
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))

        # if need to speak the execution result by tts
        #hermes.publish_start_session_notification(intent_message.site_id,"Action2 has been done")

    def intent_send_callback(self, hermes, intent_message):
        logger.info('...intent-sendadd...')
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(intent_message.intent.intent_name))

        print('[Received] confidence: {}'.format(intent_message.intent.confidence_score))
        # if need to speak the execution result by tts
        #hermes.publish_start_session_notification(intent_message.site_id,"Action2 has been done")

    # --> Master callback function
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'Rdlc14:addItemOnShoppingList':
            self.intent_add_callback(hermes, intent_message)

        if coming_intent == 'Rdlc14:deleteItemOnShoppingList':
            self.intent_delete_callback(hermes, intent_message)

        if coming_intent == 'Rdlc14:itemsOnShoppingList':
            self.intent_list_callback(hermes, intent_message)

        if coming_intent == 'Rdlc14:flushShoppingList':
            self.intent_flush_callback(hermes, intent_message)

        if coming_intent == 'Rdlc14:printShoppingList':
            self.intent_print_callback(hermes, intent_message)

        if coming_intent == 'Rdlc14:sendShoppingList':
            self.intent_send_callback(hermes, intent_message)

    # --> Register callback function and start MQTT
    def start_blocking(self):
        logger.info('...myQwitchen...')
        logger.info('Connection au MQTT broker' + MQTT_ADDR)

        with Hermes(MQTT_ADDR) as h:
            #h.subscribe_intent("Rdlc14:sendShoppingList", self.intent_send_callback).start()
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    ShoppingList()
