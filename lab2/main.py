# '''
# In the assignment you have to emulate typical CRUD operations using plain functions.

# CRUD: Create, Read (Retrieve), Update, Delete.
# Firstly, implement parsing function.
# For database emulation we can use list, i.e.,

# DATABASE = list(), can be global variable of passed into each function as
#               argument.
# '''


from datetime import datetime
import re, bcrypt

DATABASE = {'Record': [], 'User': []}


def valid_args(args: dict) -> dict:
    args_dict = {}
    for key, value in args:
        value = value.strip()
        if key == 'password':
            salt = bcrypt.gensalt()
            value_bytes = value.encode('utf-8')
            value = bcrypt.hashpw(value_bytes, salt)
        elif key == 'date':
            value = datetime(*list(map(int, value.split('.')[::-1])))
        args_dict[key] = value

    return args_dict


def parse_string(string: str) -> dict:
    """
    record: "Record(id=1, date=26.02.2004, content=Some example,
                    user=1, title=Example title)"
    user:    "User(id=1, first_name=test name, second_name=test surname,
                    email=test@test.test, password=123)"
    Return:
    dict: {'record': {"id": 1, "date": datetime.datetime, 'content':
                        'Some example',"user": 1, 'title': "Example title"}}
            or
            {'user': {"id": 1, 'first_name': 'test_name', ...,
                    "password": hash(password)}}

    """

    args_pattern = r'(\w+)\s*=\s*([\w\s.]+)'
    obj_type_pattern = r'^\s*(\w+)\s*\('

    object_name = re.findall(obj_type_pattern, string)[0]
    args = re.findall(args_pattern, string)

    return [object_name, valid_args(args)]


def create(string: str) -> dict:
    """
    Performs creation operation. Input: string with record. Output: parsed string
    converted into dict (json).

    Args:
    user (str): "User(id=1, first_name=test name, second_name=test surname,
                    email=test@test.test, password=123)"
    Returns:
    dict: user = {"id": 1, 'first_name': 'test_name', ...,
                    "poassword": hash(password) }

    """
    new_record_type, new_record = parse_string(string)

    DATABASE[new_record_type].append(new_record)

    print('Record had been created')
    return new_record


def _get_record_by_id(record_id: str, record_type: 'User' or 'Record'):
    for i in DATABASE[record_type]:
        if i['id'] == record_id:
            return i


def update(record: str) -> dict:
    """
    Performs update operation. Input: string with record. Output: parsed string
    converted into dict (json).

    Args:
      record (str): "Record(id=1, date=24.02.2004, content=Some example,
                     user=1, 'title'=Example title)"
    Returns:
      dict: record = {"id": 1, "date": datetime.datetime, 'content': 'Some example',
                      "user": 1, 'title': "Example title"}

    """

    new_record_type, new_record = parse_string(record)
    new_record_id = new_record['id']
    old_record = _get_record_by_id(new_record_id, new_record_type)

    if not old_record:
        print('Record not exist')
    else:
        for key, value in new_record.items():
            old_record[key] = value
        print('Record exist')

    return old_record


def read(record_str: str) -> dict:

    new_record_type, new_record = parse_string(record_str)

    l = []
    for i in DATABASE[new_record_type]:
        for key, value in new_record.items():
            if i.get(key) == value:
                l.append(i)
                break

    print(l)

    return l


def delete(record_str: str) -> dict:
    """
    removes record by given id. Search DATABASE, find and delete record by id from
            DATABASE.

    Args:
      record_id (int): record id.

    Returns:
      dict: record = {"id": 1, "date": datetime.datetime, 'content': 'Some example',
                      "user": 1, 'title': "Example title"}

    """
    new_record_type, new_record = parse_string(record_str)
    try:
        return DATABASE[new_record_type].pop(int(new_record['id']) - 1)
    except IndexError:
        return 'Record not exist'


def show_db(n=None):
    print(DATABASE)


if __name__ == '__main__':
    commands = {
        1: [create, 'create'],
        2: [update, 'update'],
        3: [delete, 'delete'],
        4: [read, 'read'],
        5: [show_db, 'show_db'],
        6: [..., 'exit'],
    }
    while True:
        for key, value in commands.items():
            print(f'{key}. {value[1]}')
        select = int(input('N => '))
        if select == 6:
            break
        record_str = input('Record str => ')
        commands[select][0](record_str)
