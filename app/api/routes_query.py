import dateparser
from fastapi import APIRouter
from pydantic import BaseModel
import spacy
import re

from app.utils import extract_city,parse_date,calculate_time

#The router
router = APIRouter()

#To understand the english language
nlp = spacy.load("en_core_web_sm")

#Basic route for testing
@router.get("/")
def say_hello():
    return {"message": "Hello from Query"}

#Query Class
class Query(BaseModel):
    text: str

#convert the normal eng to json
@router.post("/parse")
def parse_query(query: Query):
    doc = nlp(query.text)

    city = None
    date = None
    time = None


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
            # Try regex like "12th August"
            match2 = re.search(r"\d{1,2}(st|nd|rd|th)?\s+\w+", query.text)
            if match2:
                parsed = dateparser.parse(match2.group(0))
                if parsed:
                    date = parsed.strftime("%d-%m-%Y")

    if not time:
        match = re.search(r"\b\d{1,2}(am|pm)\b", query.text.lower())
        if match:
            time = match.group(0)

    return {
        "city": city,
        "date": date,
        "time": time
    }
