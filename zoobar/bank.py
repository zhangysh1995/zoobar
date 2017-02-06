from zoodb import *
from debug import *

import time

def new(username):
    bankdb = bank_setup()
    bank = bankdb.query(Bank).get(username)
    if bank:
        raise ValueError()
    newbank = Bank()
    newbank.username = username
    bankdb.add(newbank)
    bankdb.commit()

def transfer(sender, recipient, zoobars):
    bankdb = bank_setup()
    senderp = bankdb.query(Bank).get(sender)
    recipientp = bankdb.query(Bank).get(recipient)

    if senderp is None or recipientp is None:
        raise ValueError()

    if sender == recipient:
        return

    sender_balance = senderp.zoobars - zoobars
    recipient_balance = recipientp.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    senderp.zoobars = sender_balance
    recipientp.zoobars = recipient_balance
    bankdb.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()

def balance(username):
    db = bank_setup()
    bank = db.query(Bank).get(username)
    return bank.zoobars

def get_log(username):
    db = transfer_setup()
    return db.query(Transfer).filter(or_(Transfer.sender==username,
                                         Transfer.recipient==username))

