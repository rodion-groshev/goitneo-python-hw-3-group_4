from collections import UserDict
from datetime import datetime
from collections import defaultdict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number. Try again")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        date_format = "%d.%m.%Y"
        try:
            value = datetime.strptime(value, date_format).date()
        except ValueError:
            raise ValueError("Wrong format! Date must be in format DD.MM.YYYY")
        if value.year < 1905 or value > value.today():
            raise ValueError("Incorrect date! Check your date and try again please.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        self.phones = [Phone(new_phone) if str(p) == old_phone else p for p in self.phones]

    def find_phone(self, phone):
        return phone if phone in [str(p) for p in self.phones] else f"Phone number {phone} not found"

    def __str__(self):
        if self.birthday is None:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        else:
            return (f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, "
                    f"birthday: {self.birthday}")


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data[name]

    def show_birthday(self, name):
        return self.data[name].birthday

    def delete(self, name):
        self.data.pop(name)

    def get_birthday_per_week(self):
        default_dict = defaultdict(list)
        today = datetime.today().date()

        for user in self.data:
            name = self.data[user].name.value
            birthday = self.data[user].birthday.value
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            delta_days = (birthday_this_year - today).days
            if 0 <= delta_days < 7:
                if birthday_this_year.strftime("%A") in ["Saturday", "Sunday"] and delta_days <= 5:
                    default_dict[birthday_this_year.strftime("Monday")].append(f"{name} {birthday}")
                else:
                    default_dict[birthday_this_year.strftime("%A")].append(f"{name} {birthday}")

        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        default_dict = {day: default_dict[day] for day in week}

        for day in default_dict:
            if default_dict[day]:
                print(f"{day}: {', '.join(default_dict[day])}")


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Invalid key"
        except IndexError:
            return "Invalid index"

    return inner


@input_error
def add_contact(args, book):
    if len(args) == 3:
        name, phone, birthday = args
        record = Record(name)
        record.add_phone(phone)
        record.add_birthday(birthday)
    else:
        name, phone = args
        record = Record(name)
        record.add_phone(phone)
    book.add_record(record)
    return f"Contact {name} added."


@input_error
def add_additional_phone(args, book):
    name, phone = args
    record = book.find(name)
    record.add_phone(phone)
    return f"{phone} successfully added to contact {name} "


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return f"Birthday successfully added to the contacts {name}"


@input_error
def show_birthday(args, book):
    name = args[0]
    return f"{name}'s birthday: {book.show_birthday(name)}"


@input_error
def get_birthday(book):
    book.get_birthday_per_week()


@input_error
def change_contact(args, book):
    name, phone = args
    if name in book:
        record = book.find(name)
        record.edit_phone(record.phones[0].value, phone)
        return "Contact updated."
    else:
        return "Contact not found"


@input_error
def show_phone(args, book):
    name = args[0]
    if name in book:
        record = book.find(name)
        return ",".join(record.phones[index].value for index in range(len(record.phones)))
    else:
        return f"Contact {name} not found"


@input_error
def show_all(book):
    return "\n".join(f"{value}" for name, value in book.items())


@input_error
def del_phone(args, book):
    name, phone = args
    record = book.find(name)
    record.remove_phone(phone)
    return f"Phone: {phone} successfully remove from contact {name}"


@input_error
def del_contact(args, book):
    name = args[0]
    book.delete(name)
    return f"Contact: {name} deleted successful."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can i help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "add-phone":
            print(add_additional_phone(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthday":
            get_birthday(book)
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "remove-phone":
            print(del_phone(args, book))
        elif command == "delete-contact":
            print(del_contact(args, book))
        else:
            print(f"Invalid command {command}.")


if __name__ == "__main__":
    main()
