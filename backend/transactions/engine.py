from models import User

def validate_transaction(db, sender_id, receiver_name, amount):

    if amount is None or amount <= 0:
        return False, "Invalid amount"

    receiver = db.query(User).filter(User.first_name.ilike(receiver_name)).first()
    if not receiver:
        return False, "Receiver not found"

    sender = db.query(User).filter(User.id == sender_id).first()

    if not sender:
        return False, "Sender not found"

    if sender.customer_id == receiver_name:
        return False, "Cannot transfer to self"

    if sender.balance < amount:
        return False, "Insufficient balance"

    return True, "Valid transaction"

def execute_transaction(db, sender, receiver, amount):
    try:
        sender.balance -= amount
        receiver.balance += amount

        db.commit()
        return True
    except:
        db.rollback()
        return False
    

def mask_customer_id(customer_id):
    return "***" + customer_id[-3:]