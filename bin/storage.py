from bin.todo import Todo

_filepath = "../lists/"


def _separate_first_word(line):
    separated_str = line.split(' ', 1)
    return separated_str[1], separated_str[0]


def _get_id(line):
    separated_line, todo_id = _separate_first_word(line)
    return separated_line, int(todo_id)


class Storage(object):
        
    def __init__(self, filename):
        self._filename = _filepath + filename

    def store_todo(self, todo):
        if not isinstance(todo, Todo):
            raise TypeError("%s attribute must be set to an instance of %s" % (todo, Todo))
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
        f = open(self._filename)
        output = []
        for line in f:
            if todo_id != line.split(' ', 1)[0]:
                output.append(line)
        f.close()
        f = open(self._filename, 'w')
        f.writelines(output)
        f.close()
