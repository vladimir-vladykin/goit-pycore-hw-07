from entities import *
from errors_helper import input_error


# Description of what program can do
SUPPORTED_COMMANDS_INFO = """
Supported list of commands:
hello -> just says hi!
add 'name' 'phone' -> saves phone number by name
change 'name' 'phone' -> edits phone number by name
phone 'name' -> outputs saved phone number for this name
all -> output all saved contacts
close -> finish assistant
exit -> finish assistant
info -> information about supported commands

Make sure you follow the format of commands, and avoid spaces in phone numbers, as they are not supported."""

@input_error # use @input_error even for main() function to completely get rid of try/except here
def main():
    # greetings to user + list of supported commands
    print("Welcome to the assistant bot!")
    print(format_info())
    
    # waits for user's commands forever, untill terminal command is occurred
    contacts = {}
    address_book = AddressBook()

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

    
@input_error
def change_contact(args, address_book: AddressBook):
    name, phone = args

    # FIXME is that right? do have to support change at all? we have multiple phone numbers now
    contact_record = address_book.find(name)
    if contact_record is not None:
        contact_record.add_phone(phone)
        return "Contact changed."
    
    return "Contact changed."


@input_error
def format_info():
    return SUPPORTED_COMMANDS_INFO

if __name__ == "__main__":
    # run program
    main()