INDIAN_CITIES=["Ariyalur","Chengalpattu","Chennai",
               "Coimbatore","Cuddalore","Dharmapuri",
               "Dindigul","Erode","Kallakurichi","Kancheepuram",
               "Karur","Krishnagiri","Madurai","Mayiladuthurai",
               "Nagapattinam","Namakkal","Nilgiris","Perambalur",
               "Pudukkottai","Ramanathapuram","Ranipet","Salem",
               "Sivaganga","Tenkasi","Thanjavur","Theni","Thoothukudi",
               "Tiruchirappalli","Tirunelveli","Tirupathur","Tiruppur",
               "Tiruvallur","Tiruvannamalai","Tiruvarur","Vellore",
               "Viluppuram","Virudhunagar"
]
# to extract local cities if the NLP doesnt recognize it
def extract_city(text):
    for city in INDIAN_CITIES:
        if city.lower() in text.lower():
            return city
    return None