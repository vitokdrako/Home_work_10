from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __str__(self):
        return self.value
    
class Phone(Field):
    def __init__(self, number):
        if not self.validate_number(number):
            raise ValueError(f"Неправильний номер телефону: {number}")
        super().__init__(number)

    @staticmethod
    def validate_number(number):
        return re.fullmatch(r'\d{10}', number) is not None

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                self.phones.remove(phone)
                return f"Номер телефону {number} видалено з контакту {self.name}"
        raise ValueError(f"Номер телефону {number} не знайдено у запису {self.name}")


    def edit_phone(self, old_number, new_number):
        found_phone = self.find_phone(old_number)
        if found_phone:
            found_phone.value = new_number
            return f"Змінено номер телефону для {self.name} з {old_number} на {new_number}"
        else:
            raise ValueError(f"Номер телефону {old_number} не знайдено у запису {self.name}")
    
    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        raise ValueError(f"Номер телефону {number} не знайдено у запису {self.name}")
    
    def __str__(self):
        phones_str = "; ".join(str(phone) for phone in self.phones)
        return f"Ім'я контакту: {self.name}, телефони: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Контакт {name} видалено"
        raise ValueError(f"Контакт {name} не знайдено")   
    
def input_error(handler):
    def wrapped(*args):
        try:
            return handler(*args)
        except KeyError as e:
            return f"Error: {e} not found."
        except ValueError as e:
            return f"Error: {e}"
        except IndexError as e:
            return f"Error: {e}"
    return wrapped
    
@input_error
def hello(*args):
    return "How can I help you?"

@input_error
def add_contact(name, phone):
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return f"Added phone {phone} to contact {name}"

@input_error
def change_phone(name, old_number, new_number):
    record = book.find(name)
    if not record:
        raise KeyError(name)
    return record.change_phone(old_number, new_number)

@input_error
def show_phone(name):
    record = book.find(name)
    if not record:
        raise KeyError(name)
    phones_str = "; ".join(str(phone) for phone in record.phones)
    return f"{name}: {phones_str}"

@input_error
def show_all():
    return str(book)

@input_error
def delete_contact(name):
    book.delete(name)
    return f"Видалений контакт {name}"

handlers = {
    "hello": hello,
    "add": add_contact,
    "change": change_phone,
    "phone": show_phone,
    "show all": show_all,
    "delete": delete_contact,
}

def main():
    while True:
        user_input = input("Введіть команду: ").strip().lower()
        command_parts = user_input.split()

        if not command_parts:
            print("Команду не введено. Спробуйте ще раз.")
            continue

        command_name = ' '.join(command_parts[:2]) if command_parts[0] == 'show' else command_parts[0]
        data = command_parts[2:] if command_parts[0] == 'show' else command_parts[1:]

        if command_name in ["good bye", "close", "exit"]:
            print("До побачення!")
            break

        handler = handlers.get(command_name)

        if not handler:
            print("Невідома команда! Доступні команди: hello, add, change, phone, show all, delete.")
            continue

        try:
            result = handler(*data)
            print(result)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    book = AddressBook()
    main()