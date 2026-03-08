// Todo 관리 앱 - Practice 01 실습용 코드

export interface Todo {
  id: number;
  title: string;
  completed: boolean;
  createdAt: Date;
}

let todos: Todo[] = [];
let nextId = 1;

export function addTodo(title: string): Todo {
  const todo: Todo = {
    id: nextId++,
    title,
    completed: false,
    createdAt: new Date(),
  };
  todos.push(todo);
  return todo;
}

export function completeTodo(id: number): Todo | undefined {
  const todo = todos.find((t) => t.id === id);
  if (todo) {
    todo.completed = true;
  }
  return todo;
}

export function deleteTodo(id: number): boolean {
  const index = todos.findIndex((t) => t.id === id);
  if (index !== -1) {
    todos.splice(index, 1);
    return true;
  }
  return false;
}

export function listTodos(): Todo[] {
  return [...todos];
}

export function listCompleted(): Todo[] {
  return todos.filter((t) => t.completed);
}

export function listPending(): Todo[] {
  return todos.filter((t) => !t.completed);
}

export function clearAll(): void {
  todos = [];
  nextId = 1;
}
