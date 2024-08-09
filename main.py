from entities import *
from errors_helper import input_error


# Description of what program can do
SUPPORTED_COMMANDS_INFO = """
Supported list of commands:
hello -> just says hi!
add 'name' 'phone' -> create contact. Note that phone should be exactly 10 symbols long.
change 'name' 'old phone' 'new phone' -> edits phone number of contact.
phone 'name' -> outputs saved phone numbers of contacts.
add-birthday 'name' 'birthday' -> saves birthday for user, in 'DD.MM.YYYY' format.
show-birthday 'name' -> outputs birthday of user.
birthdays -> output all upcoming birthdays.
all -> output all saved contacts.
close -> finish assistant.
exit -> finish assistant.
info -> information about supported commands.

Make sure you follow the format of commands, and avoid spaces and plus in phone numbers, as they are not supported."""

@input_error # use @input_error even for main() function to completely get rid of try/except here
def main():
    # greetings to user + list of supported commands
    print("Welcome to the assistant bot!")
    print(format_info())
    
    # this is where our contacts lives
    address_book = AddressBook()

    # waits for user's commands forever, untill terminal command is occurred
    while True:
        user_input = input("Enter a command: ")

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "phone":
            print(find_numbers_by_name(args, address_book))
        elif command == "add-birthday":
            print(add_birthday(args, address_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            print(birthdays(args, address_book))
        elif command == "all":
            print(output_all_contacts(address_book))
        elif command == "info":
            print(format_info())
        else:
            print("Invalid command.")


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, address_book: AddressBook):
    name, phone = args

    # TODO update and make like in lesson?
    new_contact = Record(name)
    new_contact.add_phone(phone)
    address_book.add_record(new_contact)

    return "Contact added."


@input_error
def output_all_contacts(address_book: AddressBook):
    all_contacts = address_book.all_records()
    if len(all_contacts) > 0:
        return f"Here's all added contacts:\n{all_contacts}."
    else:
        return "No contacts added so far."

@input_error
def find_numbers_by_name(args, address_book: AddressBook):
    name = args[0]
    phones = address_book.find_phones(name)
    return f"Phone numbers of {name}:\n {phones}."


# TODO update for new format 
@input_error
def change_contact(args, address_book: AddressBook):
    name, phone = args

    # FIXME is that right? do have to support change at all? we have multiple phone numbers now -> user have to mention both numbers
    contact_record = address_book.find(name)
    if contact_record is not None:
        contact_record.add_phone(phone)
        return "Contact changed."
    
    return "Contact changed."

@input_error
def add_birthday(args, address_book: AddressBook):
    name, birthday = args

    record = address_book.find(name)
    record.add_birthday(birthday)

    return f"Birthday added for {name}"

@input_error
def show_birthday(args, address_book: AddressBook):
    name = args[0]
    user = address_book.find(name)
    birthday = user.birthday
    
    if birthday is not None:
        return f"Birthday of {name}'s is {birthday}"
    else:
        return f"No birthday added for user {name}"

@input_error
def birthdays(args, address_book: AddressBook):
    upcoming_birthdays = address_book.get_upcoming_birthdays()

    result = ""
    if upcoming_birthdays:
        result += "Upcoming birthdays:\n"
        for birthday_item in upcoming_birthdays:
            result += f"{birthday_item[user_key].name}: {birthday_item[congratulation_date_key]}\n"
    else:
        result += "No upcoming birthdays for now."

    return result


@input_error
def format_info():
    return SUPPORTED_COMMANDS_INFO

if __name__ == "__main__":
    # run program
    main()