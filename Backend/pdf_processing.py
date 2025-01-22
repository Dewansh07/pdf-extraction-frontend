import pdfplumber
import spacy
import re

nlp = spacy.blank("en")

def initialize_nlp():
    ruler = nlp.add_pipe("entity_ruler", last=True)
    patterns = [
        {"label": "NAME", "pattern": [{"LOWER": "name"}, {"IS_PUNCT": True, "OP": "?"}, {"LOWER": ":"}, {"TEXT": {"REGEX": "[A-Z][a-zA-Z ]+"}}]},
        {"label": "PHONE", "pattern": [{"LOWER": "phone"}, {"IS_PUNCT": True, "OP": "?"}, {"LOWER": ":"}, {"TEXT": {"REGEX": r"\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}"}}]},
        {"label": "ADDRESS", "pattern": [{"LOWER": "address"}, {"IS_PUNCT": True, "OP": "?"}, {"LOWER": ":"}, {"TEXT": {"REGEX": ".+"}}]},
    ]
    ruler.add_patterns(patterns)

initialize_nlp()

def preprocess_text(text):
    return " ".join(text.split())

def extract_details_with_nlp(text):
    doc = nlp(text)
    details = {"Name": None, "Phone": None, "Address": None}

    for ent in doc.ents:
        if ent.label_ == "NAME":
            details["Name"] = ent.text.strip()
        elif ent.label_ == "PHONE":
            details["Phone"] = ent.text.strip()
        elif ent.label_ == "ADDRESS":
            details["Address"] = ent.text.strip()
    
    if not details["Phone"]:
        phone_pattern = r"phone\s*:\s*(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9})"
        phone_match = re.search(phone_pattern, text, re.IGNORECASE)
        if phone_match:
            details["Phone"] = phone_match.group(1).strip()

    if details["Address"]:
        address_start = text.find(details["Address"])
        address_end = len(text) if "Role :" not in text else text.find("Role :")
        details["Address"] = text[address_start:address_end].strip()

    return details

def extract_details_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        extracted_text = preprocess_text("".join([page.extract_text() for page in pdf.pages]))
    
    return extract_details_with_nlp(extracted_text)
