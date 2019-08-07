#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import os

def extract_items(intent_message):
    """
        extract slot item
        used by add action, delete action (intents : addItemOnShoppingList, deleteItemOnShoppingList)
        :param intent_message
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
        :param intent_message
        :param default_media
    """

    media = default_media
    if intent_message.slots.media:
        media = intent_message.slots.media.first().value

    return media

def extract_nom(intent_message, default_user):
    """
        extract slot nom
        used by send action (intent : sendShoppingList)
        :param intent_message
        :param default_user
    """
    nom = default_user
    if intent_message.slots.nom:
        nom = intent_message.slots.nom.first().value

    return nom

def getShoppingList():
    """
        manage the shoppingList
    """
    shoppingListFile = './shoppingList.txt'
    if os.path.isfile(shoppingListFile):
        with open(shoppingListFile, mode='r', encoding='utf-8') as file_handler:
            listCourses = file_handler.readlines()

        file_handler.close()
    else:
        listCourses = []

    return listCourses

def saveShoppingList(listDeCourses):
    """
        save the shoppingList
        :param listCourses
    """
    with open('./shoppingList.txt', mode='w', encoding='utf-8') as file_handler:
        file_handler.write("  LISTE DES COURSES\n")
        file_handler.write("---------------------\n")
        for item in listDeCourses:
            file_handler.write("{}\n".format(item))

        file_handler.close()


