import {
  addTodo,
  completeTodo,
  deleteTodo,
  listTodos,
  listCompleted,
  listPending,
  clearAll,
} from "./todo";

beforeEach(() => {
  clearAll();
});

describe("addTodo", () => {
  it("should add a todo with incremental id", () => {
    const todo1 = addTodo("Buy groceries");
    const todo2 = addTodo("Walk the dog");

    expect(todo1.id).toBe(1);
    expect(todo2.id).toBe(2);
    expect(todo1.title).toBe("Buy groceries");
    expect(todo1.completed).toBe(false);
  });
});

describe("completeTodo", () => {
  it("should mark a todo as completed", () => {
    const todo = addTodo("Read a book");
    const completed = completeTodo(todo.id);

    expect(completed?.completed).toBe(true);
  });

  it("should return undefined for non-existent id", () => {
    const result = completeTodo(999);
    expect(result).toBeUndefined();
  });
});

describe("deleteTodo", () => {
  it("should remove a todo", () => {
    const todo = addTodo("Clean house");
    expect(deleteTodo(todo.id)).toBe(true);
    expect(listTodos()).toHaveLength(0);
  });

  it("should return false for non-existent id", () => {
    expect(deleteTodo(999)).toBe(false);
  });
});

describe("listTodos", () => {
  it("should return all todos", () => {
    addTodo("Task 1");
    addTodo("Task 2");
    addTodo("Task 3");

    expect(listTodos()).toHaveLength(3);
  });

  it("should return a copy (not a reference)", () => {
    addTodo("Task 1");
    const list = listTodos();
    list.pop();

    expect(listTodos()).toHaveLength(1);
  });
});

describe("filtering", () => {
  it("should filter completed and pending", () => {
    const todo1 = addTodo("Done task");
    addTodo("Pending task");
    completeTodo(todo1.id);

    expect(listCompleted()).toHaveLength(1);
    expect(listPending()).toHaveLength(1);
  });
});
