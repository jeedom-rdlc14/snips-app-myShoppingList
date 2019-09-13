#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import sys
from mailUtils import *


def extract_items(intent_message):
    """
        extract slot item
        used by add action, delete action (intents : addItemOnShoppingList, deleteItemOnShoppingList)
        :param intent_message:
    """
    items = []
    if intent_message.slots.item:
        for ajout in intent_message.slots.item.all():
            items.append(ajout.value)

    return items


def extract_media(intent_message, default_media):
    """
        extract slot media
        used by send action (intent : sendShoppingList)
        :param intent_message::
        :param default_media:
    """

    media = default_media
    if intent_message.slots.media:
        media = intent_message.slots.media.first().value

    return media


def extract_nom(intent_message, default_user):
    """
        extract slot nom
        used by send action (intent : sendShoppingList)
        :param intent_message:
        :param default_user:
    """
    nom = default_user
    if intent_message.slots.nom:
        nom = intent_message.slots.nom.first().value

    return nom


def get_shopping_list():
    """
        to load the shoppingList
    """
    shoppingListFile = "./shoppingList.txt"
    if os.path.isfile(shoppingListFile):
        with open(shoppingListFile, mode="r", encoding="utf-8") as file_handler:
            listCourses = file_handler.read().splitlines()

        file_handler.close()
    else:
        listCourses = []

    return listCourses


def save_shopping_list(listDeCourses):
    """
        save the shoppingList
        :param listDeCourses: shopping list
    """
    with open("./shoppingList.txt", mode="w", encoding="utf-8") as file_handler:
        for item in listDeCourses:
            file_handler.write("{}\n".format(item))

        file_handler.close()


def get_message_tosend(listDeCourses):
    """
        write shopping as a texwt message
        :param listDeCourses: shopping list
    """
    msgToSend = " LISTE DE COURSES\n"
    for item in listDeCourses:
        msgToSend = msgToSend + item + "\n"

    return msgToSend


def send_mail(SMTP_ADDR, SMTP_PORT, LOGIN, PASSWD, MAIL_FROM, MAIL_TO, msgToSend):
    """
        send the message to SMTP server
        :param SMTP_ADDR: smtp.domain name
        :param SMTP_PORT: port number
        :PARAM LOGIN: email
        :param PASSWD: password
        :param MAIL_FROM: mail address of the sender
        :param MAIL_TO: mail address
        :param msgToSend: message with shopping list
    """
    serveur = ServerSMTP(SMTP_ADDR, SMTP_PORT, LOGIN, PASSWD)

    exped = MAIL_FROM
    to = MAIL_TO
    cc = []
    bcc = []
    sujet = "Liste des courses"
    corps = msgToSend
    pjointes = []
    codage = "UTF-8"
    typetexte = "plain"

    try:
        message = MessageSMTP(
            exped, to, cc, bcc, sujet, corps, pjointes, codage, typetexte
        )

    except:
        print("ERREUR : err".format(err=sys.exec_info()[1]))
        sys.exit()

    response = send_smtp(message, serveur)

    return response
