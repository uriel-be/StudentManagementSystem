from enums import Gender


class Student:
    def __int__(self, id: int, name: str, age: int, gender: str, contact_info: str):
        if (age < 1 or age > 100):
            raise ValueError('age most to be between 1 and 100.')

        self.name = name
