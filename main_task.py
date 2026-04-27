from collections import UserDict
from datetime import datetime, timedelta



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            return "Invalid input."
        except KeyError:
            return "Contact not found."
    return inner


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        self.date = datetime.strptime(value, "%d.%m.%Y").date()
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def remove_phone(self, phone):
        p = self.find_phone(phone)
        if not p:
            raise ValueError
        self.phones.remove(p)

    def edit_phone(self, old, new):
        self.remove_phone(old)
        self.add_phone(new)

    def add_birthday(self, bday):
        self.birthday = Birthday(bday)


class AddressBook(UserDict):
    def add_record(self, r):
        self.data[r.name.value] = r

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name, None)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        result = []

        for r in self.data.values():
            if not r.birthday:
                continue

            b = r.birthday.date.replace(year=today.year)
            if b < today:
                b = b.replace(year=today.year + 1)

            if 0 <= (b - today).days <= 7:
                if b.weekday() == 5:
                    b += timedelta(days=2)
                elif b.weekday() == 6:
                    b += timedelta(days=1)

                result.append({
                    "name": r.name.value,
                    "birthday": b.strftime("%d.%m.%Y")
                })

        return result


def parse_input(text):
    parts = text.split()
    return parts[0].lower(), parts[1:]


@input_error
def add(args, book):
    name, phone, *_ = args
    r = book.find(name)

    if not r:
        r = Record(name)
        book.add_record(r)

    r.add_phone(phone)
    return "OK"


@input_error
def change(args, book):
    name, old, new = args
    book.find(name).edit_phone(old, new)
    return "OK"


@input_error
def phone(args, book):
    return "; ".join(p.value for p in book.find(args[0]).phones)


@input_error
def all_contacts(book):
    return "\n".join(str(r) for r in book.data.values()) or "Empty"


@input_error
def add_birthday(args, book):
    book.find(args[0]).add_birthday(args[1])
    return "OK"


@input_error
def show_birthday(args, book):
    return book.find(args[0]).birthday.value


@input_error
def birthdays(book):
    return str(book.get_upcoming_birthdays())

def main():
    book = AddressBook()
    print("Bot ready")

    while True:
        cmd, args = parse_input(input("> "))

        if cmd in ["exit", "close"]:
            break
        elif cmd == "add":
            print(add(args, book))
        elif cmd == "change":
            print(change(args, book))
        elif cmd == "phone":
            print(phone(args, book))
        elif cmd == "all":
            print(all_contacts(book))
        elif cmd == "add-birthday":
            print(add_birthday(args, book))
        elif cmd == "show-birthday":
            print(show_birthday(args, book))
        elif cmd == "birthdays":
            print(birthdays(book))
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
