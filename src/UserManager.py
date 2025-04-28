import re
from datetime import datetime

from src.User import User

class UserManager:
    def __init__(self):
        self.users = []

    def email_exists(self, email):
        for user in self.users:
            if user.email == email:
                return True
        return False

    def validate_email(self, email):
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return re.match(pattern, email) is not None

    def validate_phone_prefix(self, phone_number, country):
        country_codes = {
            "Romania": "+40",
            "USA": "+1",
            "UK": "+44",
            "France": "+33",
            "Germany": "+49",
            "Italy": "+39",
            "Spain": "+34",
            "Canada": "+5",
            "Australia": "+61",
            "India": "+91"
        }

        for c, prefix in country_codes.items():
            if phone_number.startswith(prefix):
                return country == c

        return False
    
    def create_user(self, email, username, country, phone_number, birth_date_str):
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except ValueError:
            return 400, "Invalid birth date"

        if birth_date >= datetime.today().date():
            return 400, "Birth date is in the future"

        if not self.validate_email(email):
            return 400, "Invalid email"

        if self.email_exists(email):
            return 400, "Email already exists"

        if len(username) <= 3:
            return 400, "Username too short"
        
        if len(username) >= 20:
            return 400, "Username too long"

        if not self.validate_phone_prefix(phone_number, country):
            return 400, "Phone number prefix does not match the country"

        new_user = User(email, username, country, phone_number, birth_date)
        self.users.append(new_user)
        return 200, "User successfully created"
