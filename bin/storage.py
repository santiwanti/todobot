from os import listdir
from os.path import isfile, join

from bin.todo import Todo

_filepath = "../lists/"


class StorageError(KeyError):
    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message, errors)


def _separate_first_word(line):
    separated_str = line.split(' ', 1)
    return separated_str[1], separated_str[0]


def _get_id(line):
    separated_line, todo_id = _separate_first_word(line)
    return separated_line, int(todo_id)


def _contains_id(filename, expected_id):
    with open(filename, 'r') as f:
        for line in f:
            line, todo_id = _get_id(line)
            if todo_id == expected_id:
                return True
    return False


def _remove_id(filename, todo_id):
    output = []
    with open(filename, 'r') as f:
        for line in f:
            if todo_id != _get_id(line):
                output.append(line)
    return output


def check_exists(filename):
    open(filename, 'a').close()


def belongs_to_chat(filename, chat):
    return str(filename).split('_')[0] == chat


def get_type(filename):
    return filename.split('_')[1][:-3].upper()


def get_files(file_path):
    return [f for f in listdir(file_path) if isfile(join(file_path, f))]


class Storage(object):

    @staticmethod
    def existing_lists(chat: str):
        txt = ''
        files = get_files(_filepath)
        for file in files:
            if belongs_to_chat(file, chat):
                txt += get_type(file) + '\n'
        return txt
        
    def __init__(self, filename):
        complete_name = _filepath + filename
        check_exists(complete_name)
        self._filename = complete_name

    def store_todo(self, todo):
        if not isinstance(todo, Todo):
            raise TypeError("%s attribute must be set to an instance of %s" % (todo, Todo))
        if _contains_id(self._filename, todo.id):
            raise StorageError("This id is already in use.")
        with open(self._filename, 'a') as f:
            text = str(todo.id) + ' ' + todo.description + '\n'
            f.write(text)
    
    def get_todos(self):
        todos = []
        with open(self._filename, 'r') as f:
            for line in f:
                line, todo_id = _get_id(line)
                todo_desc = line
                todos.append(Todo(todo_id, todo_desc))
        return todos
    
    def delete_todo(self, todo_id):
        if not _contains_id(self._filename, todo_id):
            raise StorageError("This id does not exist")
        remaining_lines = _remove_id(self._filename, todo_id)
        with open(self._filename, 'w') as f:
            f.writelines(remaining_lines)
