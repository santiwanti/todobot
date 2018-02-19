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


class Storage(object):
        
    def __init__(self, filename):
        self._filename = _filepath + filename

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
