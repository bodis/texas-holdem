
class Player:
    def __init__(self, name, registration_url):
        self.name = name
        self.registration_url = registration_url

    def __str__(self):
        return f"Name: {self.name}\nRegistration URL: {self.registration_url}"
