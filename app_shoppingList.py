#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from snipsTools import SnipsConfigParser
import const
from utils import (
    get_shopping_list,
    extract_nom,
    extract_media,
    extract_items,
    save_shopping_list,
    send_mail,
    get_message_tosend,
)

import logging
from logging.handlers import RotatingFileHandler

CONFIG_INI = "config.ini"


class ShoppingList(object):
    """
        Class used to wrap action code with mqtt connection
    """

    def __init__(self):
        self.start_blocking()

    @staticmethod
    def terminate_feedback(hermes, intent_message, mode="default"):
        """
            feedback reply // future function
            :param hermes:
            :param intent_message:
            :param mode:
        """
        if mode == "default":
            hermes.publish_end_session(intent_message.session_id, "")
        else:
            hermes.publish_end_session(intent_message.session_id, "")

    def intent_add_callback(self, hermes, intent_message):
        """
            callback function, to the addItemOnShoppingList intent

            :param hermes:
            :param intent_message:
        """

        # action code goes here...
        receivedMessage = "[Received] intent: {}".format(
            intent_message.intent.intent_name
        )
        logger.info(receivedMessage)
        confidenceMessage = "[Received] confidence: : " + str(
            intent_message.intent.confidence_score
        )
        logger.info(confidenceMessage)

        itemsToAdd = extract_items(intent_message)
        texttospeak = ""

        for item in itemsToAdd:
            if item not in listDeCourses:
                listDeCourses.append(item)
                texttospeak = texttospeak + item + ", "

        messagetospeak = const.ADD_OK.format(texttospeak=texttospeak)

        logger.info(messagetospeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(
            intent_message.site_id, messagetospeak, "Shopping_list_APP"
        )

    def intent_delete_callback(self, hermes, intent_message):
        """
            callback function, to the deleteItemOnShoppingList intent

            :param hermes:
            :param intent_message:
        """

        # action code ...
        receivedMessage = "[Received] intent: {}".format(
            intent_message.intent.intent_name
        )
        logger.info(receivedMessage)
        confidenceMessage = "[Received] confidence: : " + str(
            intent_message.intent.confidence_score
        )
        logger.info(confidenceMessage)

        texttospeak = ""
        itemsToDel = extract_items(intent_message)
        for item in itemsToDel:
            if item in listDeCourses:
                listDeCourses.remove(item)
                texttospeak = texttospeak + item + ", "

        messagetospeak = const.DEL_OK.format(texttospeak=texttospeak)
        logger.info(messagetospeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(
            intent_message.site_id, messagetospeak, "Shopping_ist_APP"
        )

    def intent_flush_callback(self, hermes, intent_message):
        """
            callback function, to the flushShoppingList intent

            :param hermes:
            :param intent_message:
        """
        # action code ...
        receivedMessage = "[Received] intent: {}".format(
            intent_message.intent.intent_name
        )
        logger.info(receivedMessage)
        confidenceMessage = "[Received] confidence: : " + str(
            intent_message.intent.confidence_score
        )
        logger.info(confidenceMessage)

        lengthlist = len(listDeCourses)
        texttospeak = ""
        for item in listDeCourses:
            listDeCourses.remove(item)
            texttospeak = texttospeak + item + ", "

        messagetospeak = const.FLUSH_OK.format(length=lengthlist, texttospeak=texttospeak)
        logger.info(messagetospeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(
            intent_message.site_id, messagetospeak, "Shopping_ist_APP"
        )

    def intent_list_callback(self, hermes, intent_message):
        """
            callback function, to the itemsOnShoppingList intent

            :param hermes:
            :param intent_message:
        """
        # action code ...
        receivedMessage = "[Received] intent: {}".format(
            intent_message.intent.intent_name
        )
        logger.info(receivedMessage)
        confidenceMessage = "[Received] confidence: : " + str(
            intent_message.intent.confidence_score
        )
        logger.info(confidenceMessage)

        texttospeak = ""
        lengthlist = len(listDeCourses)
        if lengthlist == 0:
            messagetospeak = const.LIST_VIDE
        else:
            for item in listDeCourses:
                texttospeak = texttospeak + item + ", "

            messagetospeak = const.LIST_OK.format(length=lengthlist, texttospeak=texttospeak)

        logger.info(messagetospeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(
            intent_message.site_id, messagetospeak, "Shopping_ist_APP"
        )

    def intent_print_callback(self, hermes, intent_message):
        """
            callback function, to the printShoppingList intent

            :param hermes:
            :param intent_message:
        """
        # action code ...
        receivedMessage = "[Received] intent: {}".format(
            intent_message.intent.intent_name
        )
        logger.info(receivedMessage)
        confidenceMessage = "[Received] confidence: : " + str(
            intent_message.intent.confidence_score
        )
        logger.info(confidenceMessage)

        if len(listDeCourses) == 0:
            messagetospeak = const.PRINT_VIDE
        else:
            # writing list to file
            save_shopping_list(listDeCourses)
            # send file to printer
            messagetospeak = const.PRINT_OK.format(imp='')

        logger.info(messagetospeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(
            intent_message.site_id, messagetospeak, "Shopping_ist_APP"
        )

    def intent_send_callback(self, hermes, intent_message):
        """
            callback function, to the sendShoppingList intent

            :param hermes:
            :param intent_message:
        """
        # action code ...
        receivedmessage = "[Received] intent: {}".format(
            intent_message.intent.intent_name
        )
        logger.info(receivedmessage)
        confidenceMessage = "[Received] confidence: : " + str(
            intent_message.intent.confidence_score
        )
        logger.info(confidenceMessage)

        media = extract_media(intent_message, "mail")
        user = extract_nom(intent_message, "Alain")

        if len(listDeCourses) == 0:
            messagetospeak = const.SENT_VIDE
        else:
            # writing list to file and send
            save_shopping_list(listDeCourses)
            # send to user
            msgToSend = get_message_tosend(listDeCourses)
            response = send_mail(
                SMTP_ADDR, SMTP_PORT, LOGIN, PASSWD, MAIL_FROM, MAIL_TO, msgToSend
            )
            if response == "":
                messagetospeak = const.SENT_OK.format(media=media, user=user)
            else:
                messagetospeak = const.SENT_KO.format(media=media, user=user)

        logger.info(messagetospeak)

        self.terminate_feedback(hermes, intent_message)
        # speak the execution result by tts
        hermes.publish_start_session_notification(
            intent_message.site_id, messagetospeak, "Shopping_ist_APP"
        )

    def master_intent_callback(self, hermes, intent_message):
        """
            Master callback function, triggered everytime an intent is recognized
            :param hermes:
            :param intent_message:
        """
        coming_intent = intent_message.intent.intent_name
        if coming_intent == "Rdlc14:addItemOnShoppingList":
            self.intent_add_callback(hermes, intent_message)
        if coming_intent == "Rdlc14:deleteItemOnShoppingList":
            self.intent_delete_callback(hermes, intent_message)
        if coming_intent == "Rdlc14:itemsOnShoppingList":
            self.intent_list_callback(hermes, intent_message)
        if coming_intent == "Rdlc14:flushShoppingList":
            self.intent_flush_callback(hermes, intent_message)
        if coming_intent == "Rdlc14:printShoppingList":
            self.intent_print_callback(hermes, intent_message)
        if coming_intent == "Rdlc14:sendShoppingList":
            self.intent_send_callback(hermes, intent_message)

    def start_blocking(self):
        """
            Register callback function and start MQTT bus.
        """
        logger.info("...myShoppingList...")
        logger.info("Connection au MQTT broker" + MQTT_ADDR)

        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()


# main function


if __name__ == "__main__":
    try:
        config = SnipsConfigParser.read_configuration_file(CONFIG_INI)

    except:
        print("config --> vide")
        config = None

    MQTT_IP_ADDR = config["global"].get("mqtt_host")
    MQTT_PORT = config["global"].get("mqtt_port")
    MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

    MEDIA = config["secret"].get("default_media")
    USERNAME = config["secret"].get("default_user")
    MAIL_TO = config["secret"].get("mail_default_user")
    SMTP_ADDR = config["secret"].get("smtp_server")
    SMTP_PORT = config["secret"].get("smtp_port")
    LOGIN = config["secret"].get("smtp_login")
    PASSWD = config["secret"].get("smtp_passwd")
    MAIL_FROM = config["secret"].get("mail_from")

    locale = config["secret"].get("locale")

    # logging config
    logging.basicConfig(
        format="%(asctime)s - [%(levelname)s] - %(message)s",
        level=logging.INFO,
        filename="myShoppingList.log",
        filemode="w",
    )

    logger = logging.getLogger("myShoppingList")
    handler = logging.StreamHandler()
    file_handler = RotatingFileHandler('/var/log/supervisor/shoppinglist.log', maxBytes=10000, backupCount=3)
    logger.addHandler(file_handler)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


    # get the shopping list
    listDeCourses = get_shopping_list()

    resultToSpeak = ""

    try:
        ShoppingList()

    except KeyboardInterrupt:
        logger.info("...myQShoppingList --> stop ...")
