#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#

import os
from smtplib import SMTP
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate

class ServeurSMTP(object):

    def __init__(self, address, port, login, mdpass):
        """
            conserve les paramètres d'un compte mail sur un serveur SMTP
        """
        self.address = address
        self.port = port
        self.login = login
        self.mdpass = mdpass

class MessageSMTP(object):

    def __init__(self, exped="", to=(), cc=(), bcc=(), sujet="", corps="", pjointes=(), codage='UTF-8', typetexte='plain'):
        """
            build a mail object with params
        """
        self.expediteur = exped

        if isinstance(to, str):
            to = to.split(';')

        if to == [] or to == ['']:
            raise ValueError("failed: no to.")

        if sujet == '':
            raise ValueError("failed: no subject.")

        if isinstance(cc, str):
            cc = cc.split(';')

        if isinstance(bcc, str):
            bcc = bcc.split(';')

        if isinstance(pjointes, str):
            pjointes = pjointes.split(';')

        if codage == "":
            codage = 'UTF-8'

        if not pjointes:
            # there is no attached piece
            msg = MIMEText(corps, typetexte, _charset=codage)
        else:
            # message "multipart" within one or more attached pieces
            msg = MIMEMultipart('alternatives')

        msg['From'] = exped
        msg['To'] = ', '.join(to)
        msg['Cc'] = ', '.join(cc)
        msg['Bcc'] = ', '.join(bcc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = sujet
        msg['Charset'] = codage
        msg['Content-Type'] = 'text/' + typetexte + '; charset=' + codage

        if pjointes:
            msg.attach(MIMEText(corps, typetexte, _charset=codage))

            # add attached piece
            for file in pjointes:
                part = MIMEBase('application', "octet-stream")
                try:
                    with open(file, "rb") as f:
                        part.set_payload(f.read())
                except Exception as errMsg:
                    raise ValueError("failed when reading attached file(" + str(errMsg) + ")")
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file),)
                msg.attach(part)

        self.mail = msg.as_string()
        self.destinataires = to
        self.destinataires.extend(cc)
        self.destinataires.extend(bcc)

def send_smtp(message, server):
    """
        send message to the smtp server
    """

    smtp = None
    try:
        smtp = SMTP(server.address, server.port)

    except Exception as msgerr:
        print(type(msgerr))
        return "connection to SMTP server failed : (" + str(msgerr) + ")"

    # mode debug to trace
    # smtp.set_debuglevel(1)

    if server.login != "":
        try:
            response = smtp.login(server.login, server.mdpass)

        except Exception as msgerr:
            print(type(msgerr))
            return "failed : bad login or password (" + str(msgerr) + ")"

    # send the mail
    try:
            response = smtp.sendmail(message.expediteur, message.destinataires, message.mail)

    except Exception as msgerr:
        print(type(msgerr))
        return 'failed to send mail (' + str(msgerr) + ')'

    smtp.quit()
    # success returns an empty string
    return ""
