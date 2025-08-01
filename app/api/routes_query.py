import dateparser
from fastapi import APIRouter
from pydantic import BaseModel
import spacy
import re
import random
from datetime import datetime
from app.ml import predictor
from app.utils import extract_city, parse_date, calculate_time, nlp_to_ml

router = APIRouter()
nlp = spacy.load("en_core_web_sm")

@router.get("/")
def say_hello():
    return {"message": "Hello from Query"}

class Query(BaseModel):
    text: str

# ✅ Updated logic here
def generate_temperature(message: str):
    message_lower = message.lower()
    if "no rain" in message_lower:
        return random.choice([29, 30, 31, 32])  # Warm temp
    elif "rain" in message_lower:
        return random.choice([24, 25, 26, 27])  # Cool temp
    else:
        return random.choice([29, 30, 31, 32])  # Default fallback

@router.post("/parse")
def parse_query(query: Query):
    doc = nlp(query.text)

    city = None
    date = None
    time = None
    current_time = datetime.now().strftime("%H:%M")
    relative_time = calculate_time.resolve_relative_time(query.text)

    for ent in doc.ents:
        if ent.label_ == "GPE" and not city:
            city = ent.text
        if not city:
            city = extract_city.extract_city(query.text)
        elif ent.label_ == "DATE" and not date:
            date = parse_date.parse_natural_date(ent.text)
        elif ent.label_ == "TIME" and not time:
            time = ent.text

    if relative_time:
        date = relative_time.strftime("%d-%m-%Y")
        time = str(int(relative_time.strftime("%I"))) + relative_time.strftime("%p").lower()

    if not date:
        match = re.search(r"\d{2}-\d{2}-\d{4}", query.text)
        if match:
            date = match.group(0)
        else:
            match2 = re.search(r"\d{1,2}(st|nd|rd|th)?\s+\w+", query.text)
            if match2:
                parsed = dateparser.parse(match2.group(0))
                if parsed:
                    date = parsed.strftime("%d-%m-%Y")

    if not time:
        nlp_to_ml_prop = nlp_to_ml.convert_to_isRain_format(city, date, current_time)
        if nlp_to_ml_prop["date"] and nlp_to_ml_prop["city"] and nlp_to_ml_prop["time"]:
            message = predictor.isRain(nlp_to_ml_prop["date"], nlp_to_ml_prop["city"], nlp_to_ml_prop["time"])
            temperature = generate_temperature(message)
            return {
                "message": message,
                "date": date,
                "city": city,
                "time": nlp_to_ml_prop["time"],
                "temperature": f"{temperature}°C"
            }
        match = re.search(r"\b\d{1,2}(am|pm)\b", query.text.lower())
        if match:
            time = match.group(0)

    if date and time and city:
        nlp_to_ml_prop = nlp_to_ml.convert_to_isRain_format(city, date, time)
        if nlp_to_ml_prop["date"] and nlp_to_ml_prop["city"] and nlp_to_ml_prop["time"]:
            message = predictor.isRain(nlp_to_ml_prop["date"], nlp_to_ml_prop["city"], nlp_to_ml_prop["time"])
            temperature = generate_temperature(message)
            return {
                "message": message,
                "date": date,
                "city": city,
                "time": time,
                "temperature": f"{temperature}°C"
            }
        elif nlp_to_ml_prop["date"] and nlp_to_ml_prop["city"] and not nlp_to_ml_prop["time"]:
            message = predictor.isRain(nlp_to_ml_prop["date"], nlp_to_ml_prop["city"], current_time)
            temperature = generate_temperature(message)
            return {
                "message": message,
                "date": date,
                "city": city,
                "time": time,
                "temperature": f"{temperature}°C"
            }
        else:
            return {"message": "Not enough data"}
    else:
        return {"message": "Not enough data"}
