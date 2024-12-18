from abc import ABC, abstractmethod

class ThePerson(ABC):
    @abstractmethod
    def __init__(self, fullname, gender, age, dateofbirth, contact, email):
        self.fullname = fullname
        self.gender = gender
        self.age = age 
        self.dateofbirth = dateofbirth
        self.contact = contact
        self.email = email