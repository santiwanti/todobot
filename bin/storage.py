from bin.todo import Todo


def store_todo(filename, todo):
    if not isinstance(todo, Todo):
            raise TypeError("%s attribute must be set to an instance of %s" % (todo, Todo))
    with open(filename, 'a') as f:
        text = str(todo.id) + ' ' + todo.description + '\n'
        f.write(text)


def _separate_first_word(line):
    separated_str = line.split(' ', 1)
    return separated_str[1], separated_str[0]


def _get_id(line):
    separated_line, todo_id = _separate_first_word(line)
    return separated_line, int(todo_id)


def get_todos(filename):
    todos = []
    with open(filename, 'r') as f:
        for line in f:
            line, todo_id = _get_id(line)
            todo_desc = line
            todos.append(Todo(todo_id, todo_desc))
    return todos
