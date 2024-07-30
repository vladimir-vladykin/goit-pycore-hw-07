from collections import UserDict
from datetime import datetime, date, timedelta

# TODO small clean up?
PHONE_LENGTH = 10
user_key = "user"
birthday_key = "birthday"
congratulation_date_key = "congratulation_date"
date_pattern = "%Y.%m.%d"
days_of_upcoming_range = 7
iso_saturday = 6
iso_sunday = 7


# Base class for fields in Records.
# Implements holding of some data as string,
# and rendering of this data via __str__ method.
class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    # hack for print list of Fields easily
    def __repr__(self):
         return self.__str__()

# Name of user.
# Note that name cannot be empty, exception will be raised otherwise.
class Name(Field):
	
    def __init__(self, value: str):
        if len(value) == 0:
            raise ValueError("Empty name is not supported")
        
        super().__init__(value)
    

# Phone of user.
# Note that it's strongly required that phone contains only numbers, and exactly
# 10 numbers. Exception will be thrown if this condition is not fulfilled.
class Phone(Field):
    def __init__(self, value: str):
        if len(value) != PHONE_LENGTH:
            raise ValueError(f"Phone length is not correct, it supposed to have {PHONE_LENGTH} symbols")
        
        if not value.isdigit():
            raise ValueError("Phone number is supposed to contain only digits")

        super().__init__(value)

    # matters for indexing in list of phones
    def __eq__(self, other):
        return self.value == other.value
    

class Birthday(Field):
    raw_date_pattern = "%d.%m.%Y"

    def __init__(self, value: str):
        try:
            super().__init__(datetime.strptime(value, Birthday.raw_date_pattern).date())
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        

# One Record corresponds to single user, contains name and can contain some phone numbers
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"
    
    # hack for print list of Records easily
    def __repr__(self):
         return self.__str__()
    
    # Note that phone sould contain only numbers and have exactly 10 symbols
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        self.phones.remove[Phone(phone)]

    def edit_phone(self, phone: str, new_phone: str):
        # since Phone implements __eq__(), it's easy to work with list of Phones
        phone_object = Phone(phone)
        if phone_object not in self.phones:
            # we don't have such phone, therefore it's cannot be edited
            return
        
        # replace old phone object with new one
        existing_phone_index = self.phones.index(phone_object)
        self.phones[existing_phone_index] = Phone(new_phone)
        

    def find_phone(self, phone: str) -> Phone:
        for maybe_phone in self.phones:
            if maybe_phone.value == phone:
                return maybe_phone
            
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)
    


# Contains all info about users and their phone numbers.
# Raw user's name is a key for each record
class AddressBook(UserDict):
       
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name: str) -> Record:
        return self.data[name]
    
    def delete(self, name: str):
        if name not in self.data:
            # unknown name, nothing to remove
            return 
        
        self.data.pop(name)

    def all_records(self) -> list[Record]:
        return list(self.data.values())
    
    def find_phones(self, name: str) -> list[Record]:
        return self.data[name].phones

    # Returns list of user's records, which has upcoming birthday
    def get_upcoming_birthdays(self) -> list:
        current_date = datetime.today().date()
        current_year = current_date.year

        # result is gonna be list with dicts, each with fields like "name" and "congratulation_date"
        upcoming_birthdays_result = []

        # iterate throudg users to find out who has upcoming birthday
        for record in self.data.values():

            # parse user's birthdate
            # birthday_date = datetime.strptime(user[birthday_key], date_pattern).date()
            birthday_date = record.birthday
            
            # figure out date of celebration this year 
            birthday_month = birthday_date.month
            birthday_day = birthday_date.day    
            this_year_birthday_date = date(current_year, birthday_month, birthday_day)
            
            is_birthday_passed = this_year_birthday_date < current_date

            congrats_date: date
            if is_birthday_passed:
                # we will check for date in next year
                congrats_date = date(current_year + 1, birthday_month, birthday_day)
            else:
                congrats_date = this_year_birthday_date

            
            # we have to move congrats date if it's on weekend
            congrats_day_of_week = congrats_date.isoweekday()
            is_congrats_date_in_weekend = congrats_day_of_week >= iso_saturday
            if is_congrats_date_in_weekend:
                # we will add one day is this is Sunday, and two if this is Saturday
                days_factor = 1 if congrats_day_of_week == iso_sunday else 2
                congrats_date = congrats_date + timedelta(days=days_factor)


            
            # we now have final congrats date, now let's figure out should we 
            # include it in upcoming list

            if (congrats_date.toordinal() - current_date.toordinal()) <= days_of_upcoming_range:
                upcoming_birthdays_result.append(
                    {
                        user_key: record, 
                        congratulation_date_key: datetime.strftime(congrats_date, date_pattern)
                    }
                )
            # otherwise congrats date is not soon enough, so we do not consider it's as upcoming for now


        return upcoming_birthdays_result

        