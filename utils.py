#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

def extract_items(intent_message):
    """
        extract slot item
        used by add action, delete action (intents : addItemOnShoppingList, deleteItemOnShoppingList)
        :param: intent_message
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
        :param: intent_message
        :param: default_media
    """

    media = default_media
    if intent_message.slots.media:
        media = intent_message.slots.media.first().value

    return media

def extract_nom(intent_message, default_user):
    """
        extract slot nom
        used by send action (intent : sendShoppingList)
        :param: intent_message
        :param: default_user
    """'
    nom = default_user
    if intent_message.slots.nom:
        media = intent_message.slots.nom.first().value

    return nom

def getShoppingList():
    """
        manage the shoppingList
    """

    panier = []

    return panier