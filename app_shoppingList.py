#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from snipsTools import SnipsConfigParser
import action_add as actionAdd
import action_delete  as actionDelete
import action_flush as actionFlush
import action_list as actionList
import action_print as actionPrint
import action_send as actionSend
from utils import getShoppingList, extract_nom, extract_media, extract_items

import logging

CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

lang = "FR"

logging.basicConfig(format='%(asctime)s [%(threadName)s] - [%(levelname)s] - %(message)s', level=logging.INFO,
                    filename='myShoppingList.log', filemode='w'
                    )

logger = logging.getLogger('myShoppingList')
logger.addHandler(logging.StreamHandler())

#get the shopping list
listedecourses = getShoppingList()

resultToSpeak = ''

class ShoppingList(object):
    """
        Class used to wrap action code with mqtt connection
    """

    def __init__(self):
        """
        get the configuration if needed
        """
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        # start listening to MQTT
        self.start_blocking()


    def terminate_feedback(self, hermes, intent_message, mode='default'):
        """
            feedback reply // future function
            :param hermes:
            :param intent_message:
            :param mode:
        """
        if mode == 'default':
            hermes.publish_end_session(intent_message.session_id, "")
        else:
            #### more design
            hermes.publish_end_session(intent_message.session_id, "")

    def intent_add_callback(self, hermes, intent_message):
        """
            callback function, to the addItemOnShoppingList intent

            :param hermes:
            :param intent_message:
        """

        # action code goes here...
        receivedMessage = '[Received] intent: {}'.format(intent_message.intent.intent_name)
        logger.info(receivedMessage)
        confidenceMessage = '[Received] confidence: : ' + str(intent_message.intent.confidence_score)
        logger.info(confidenceMessage)

        itemsToAdd = extract_items(intent_message)
        textToSpeak = ''

        for item in itemsToAdd:
            if item not in listedecourses:
                Listedecourses.append(item)
                textToSpeak = textToSpeak + item + ', '

        messageToSpeak = textToSpeak + 'ajouté à la liste des courses.'
        logger.info(messageToSpeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, messageToSpeak, 'Shopping_list_APP')

    def intent_delete_callback(self, hermes, intent_message):
        """
            callback function, to the deleteItemOnShoppingList intent

            :param hermes:
            :param intent_message:
        """

        # action code ...
        receivedMessage = '[Received] intent: {}'.format(intent_message.intent.intent_name)
        logger.info(receivedMessage)
        confidenceMessage = '[Received] confidence: : ' + str(intent_message.intent.confidence_score)
        logger.info(confidenceMessage)

        textToSpeak = ''
        itemsToDel = extract_items(intent_message)
        for item in itemsToDel:
            if item in listedecourses:
                listedecourses.remove(item)
                textToSpeak = textToSpeak + item + ', '

        messageToSpeak = textToSpeak + 'retiré de la liste des courses.'
        logger.info(messageToSpeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, messageToSpeak, 'Shopping_ist_APP')

    def intent_flush_callback(self, hermes, intent_message):
        """
            callback function, to the flushShoppingList intent

            :param hermes:
            :param intent_message:
        """
        # action code ...
        receivedMessage = '[Received] intent: {}'.format(intent_message.intent.intent_name)
        logger.info(receivedMessage)
        confidenceMessage = '[Received] confidence: : ' + str(intent_message.intent.confidence_score)
        logger.info(confidenceMessage)

        lengthListe = len(listedecourses)
        textToSpeak = ''
        for item in listedecourses:
            listedecourses.remove(item)
            textToSpeak = textToSpeak + item + ', '

        messageToSpeak = lengthListe + ' produits ' + textToSpeak + ' ont été retirés de la liste des courses.'
        logger.info(messageToSpeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, messageToSpeak, 'Shopping_ist_APP')

    def intent_list_callback(self, hermes, intent_message):
        """
            callback function, to the itemsOnShoppingList intent

            :param hermes:
            :param intent_message:
        """
        # action code ...
        receivedMessage = '[Received] intent: {}'.format(intent_message.intent.intent_name)
        logger.info(receivedMessage)
        confidenceMessage = '[Received] confidence: : ' + str(intent_message.intent.confidence_score)
        logger.info(confidenceMessage)

        textToSpeak = ''
        if len(panier) == 0:
            messageToSpeak = 'Le panier est vide'
        else:
            for item in listedecourses:
                textToSpeak = textToSpeak + item + ', '

        messageToSpeak = 'Tu as ' + textToSpeak + 'dans ta liste des courses.'

        logger.info(messageToSpeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, messageToSpeak, 'Shopping_ist_APP')

    def intent_print_callback(self, hermes, intent_message):
        """
            callback function, to the printShoppingList intent

            :param hermes:
            :param intent_message:
        """
        # action code ...
        receivedMessage = '[Received] intent: {}'.format(intent_message.intent.intent_name)
        logger.info(receivedMessage)
        confidenceMessage = '[Received] confidence: : ' + str(intent_message.intent.confidence_score)
        logger.info(confidenceMessage)


        if len(listedecourses) == 0:
            messageToSpeak = "Le panier est vide. Pas d'impression"'
        else:
            # writing list to file and print

            messageToSpeak = "La liste des courses a été envoyée à l'imprimante."

        logger.info(messageToSpeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, messageToSpeak, 'Shopping_ist_APP')

    def intent_send_callback(self, hermes, intent_message):
        """
            callback function, to the sendShoppingList intent

            :param hermes:
            :param intent_message:
        """
        # action code ...
        receivedMessage = '[Received] intent: {}'.format(intent_message.intent.intent_name)
        logger.info(receivedMessage)
        confidenceMessage = '[Received] confidence: : ' + str(intent_message.intent.confidence_score)
        logger.info(confidenceMessage)

        media = extract_media(intent_message, default_media)
        utilisateur = extract_nom(intent_message, default_user)

        if len(listedecourses) == 0:
            messageToSpeak = "Le liste des courses vide. Pas d'envoi."
        else:
            # writing list to file and send

            messageToSpeak = "La liste des courses a été envoyée sur " + media

        logger.info(messageToSpeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, messageToSpeak, 'Shopping_ist_APP')

    def master_intent_callback(self, hermes, intent_message):
        """
            Master callback function, triggered everytime an intent is recognized
            :param hermes:
            :param intent_message:
        """
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

    def start_blocking(self):
        """
            Register callback function and start MQTT bus.
        """
        logger.info('...myShoppingList...')
        logger.info('Connection au MQTT broker' + MQTT_ADDR)

        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()


# main function
if __name__ == "__main__":
    try:
        ShoppingList()

    except KeyboardInterrupt:
        logger.info('...myQShoppingList --> stop ...')
