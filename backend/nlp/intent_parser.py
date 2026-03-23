import spacy
import re

nlp = spacy.load("en_core_web_sm")

# 🔹 Preprocessing
def preprocess(text):
    text = text.lower()
    text = text.replace("rupees", "").replace("rs", "")
    return text.strip()

# 🔹 Intent Detection
def detect_intent(text):
    if any(word in text for word in ["send", "transfer", "pay"]):
        return "TRANSFER_MONEY"
    elif any(word in text for word in ["balance", "money left", "account balance"]):
        return "CHECK_BALANCE"
    elif any(word in text for word in ["history", "transactions", "statement"]):
        return "VIEW_HISTORY"
    else:
        return "UNKNOWN"

# 🔹 Extract Amount
def extract_amount(text):
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None

# 🔹 Extract Receiver
def extract_receiver(doc):
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

# 🔹 MAIN FUNCTION
def parse_command(text):
    cleaned = preprocess(text)

    doc = nlp(cleaned)

    intent = detect_intent(cleaned)
    amount = extract_amount(cleaned)
    receiver = extract_receiver(doc)

    return {
        "intent": intent,
        "amount": amount,
        "receiver": receiver
    }