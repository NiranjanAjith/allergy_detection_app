import os
import requests
from together import Together
from io import BufferedReader
import base64
from itertools import zip_longest
from PIL import Image
from pyzbar.pyzbar import decode as decode_barcodes
import pytesseract

TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "Default_API_Key")
LLM_NAME = os.getenv("TOGETHER_LLM_NAME", "deepseek-ai/DeepSeek-R1")

try:
    client = Together(api_key=TOGETHER_API_KEY)
except:
    client = Together()

def extract_qr_and_text(image_file: BufferedReader) -> tuple[list[str], str]:
    """Extracts barcode/QR code content and OCR text with layout from the image."""
    image = Image.open(image_file).convert("RGB")
    
    # Reset file pointer for re-reads
    image_file.seek(0)

    # Extract QR/barcode data
    qr_data = [barcode.data.decode("utf-8") for barcode in decode_barcodes(image)]

    # OCR with layout (preserve structure like tables)
    ocr_data = pytesseract.image_to_string(image, config="--psm 6")  # psm 6 = Assume a single uniform block of text

    return qr_data, ocr_data

def generate_summary(ingredients: list[str], profile: dict, risk_scores: list[float], image_file: BufferedReader = None) -> str:

    # Prompt Pieces
    ingredient_info = "\n".join(
        f"- {ing}: Risk Score {score:.2f}"
        for ing, score in zip_longest(ingredients, risk_scores, fillvalue=0.1)
    )


    allergies = ", ".join(profile.get("allergies", [])) or "no known allergies"
    
     # Optionally use vision description
    vision_description = ""
    if image_file:
        try:
            qr_data, ocr_data = extract_qr_and_text(image_file)
            vision_description = "\nImage Analysis:\n"
            if qr_data:
                vision_description += "QR/Barcode data:\n" + "\n".join(f"- {item}" for item in qr_data) + "\n"
            if ocr_data.strip():
                vision_description += "OCR Text:\n" + ocr_data.strip()
        except Exception as e:
            vision_description = "\nImage Analysis failed."

    # Full Prompt
    prompt = "\n".join((
        f"User has the following allergy profile: {allergies}.",
        "Here are the scanned ingredients and their corresponding risk scores:",
        ingredient_info,
        vision_description,
        "Based on the allergy profile and scores, provide a short, clear risk summary.",
        "Advise whether it's safe to consume, highlight risky ingredients."
    ))
    
    try:
        completion = client.chat.completions.create(
            model=LLM_NAME,
            messages=[
                {"role": "system", "content": "You are a medical assistant specialized in allergies."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            top_p=0.9,
        )

        return completion.choices[0].message.content
    
    except:
        payload = {
            "model": LLM_NAME,
            "messages": [
                {"role": "system", "content": "You are a medical assistant specialized in allergies."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "top_p": 0.9,
        }

        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
