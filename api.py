from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import spacy
import re

app = Flask(__name__)
CORS(app)

# Load spaCy NLP model
nlp = spacy.blank("en")  # Using a blank model for simplicity

# Add patterns using EntityRuler
def add_custom_ner(nlp):
    ruler = nlp.add_pipe("entity_ruler", last=True)

    # Refined patterns for Name, Phone, and Address
    patterns = [
        {"label": "NAME", "pattern": [{"LOWER": "name"}, {"IS_PUNCT": True, "OP": "?"}, {"LOWER": ":"}, {"TEXT": {"REGEX": "[A-Z][a-zA-Z ]+"}}]},
        {"label": "PHONE", "pattern": [{"LOWER": "phone"}, {"IS_PUNCT": True, "OP": "?"}, {"LOWER": ":"}, {"TEXT": {"REGEX": r"\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}"}}]},
        {"label": "ADDRESS", "pattern": [{"LOWER": "address"}, {"IS_PUNCT": True, "OP": "?"}, {"LOWER": ":"}, {"TEXT": {"REGEX": ".+"}}]},
    ]

    ruler.add_patterns(patterns)

# Add the custom NER pipeline
add_custom_ner(nlp)

# Function to preprocess text
def preprocess_text(text):
    # Remove extra spaces and normalize text
    return " ".join(text.split())

# Function to extract details using NLP
def extract_details_with_nlp(text):
    doc = nlp(text)
    details = {"Name": None, "Phone": None, "Address": None}

    for ent in doc.ents:
        if ent.label_ == "NAME":
            details["Name"] = ent.text.strip()
        elif ent.label_ == "PHONE":
            details["Phone"] = ent.text.strip()
        elif ent.label_ == "ADDRESS":
            # Handle multi-line address extraction
            details["Address"] = ent.text.strip()
    
    # Fallback for phone number extraction
    if not details["Phone"]:
        phone_pattern = r"phone\s*:\s*(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9})"
        phone_match = re.search(phone_pattern, text, re.IGNORECASE)
        if phone_match:
            details["Phone"] = phone_match.group(1).strip()

    # Fallback: Check for address continuation
    if details["Address"]:
        address_start = text.find(details["Address"])
        address_end = len(text) if "Role :" not in text else text.find("Role :")
        details["Address"] = text[address_start:address_end].strip()

    return details


@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400

    # Process the PDF
    with pdfplumber.open(file) as pdf:
        # Extract text from PDF and preprocess it
        extracted_text = preprocess_text("".join([page.extract_text() for page in pdf.pages]))
        print("Extracted Text:", extracted_text)  # Debug log
    
    # Use NLP to extract details
    extracted_details = extract_details_with_nlp(extracted_text)
    print("Extracted Details:", extracted_details)

    return jsonify(extracted_details)


if __name__ == '__main__':
    app.run(debug=True)
