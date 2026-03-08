import { TaskManager, Task } from './app';

describe('TaskManager', () => {
  let manager: TaskManager;

  beforeEach(() => {
    manager = new TaskManager();
  });

  describe('createTask', () => {
    it('should create a task with title and description', () => {
      const task = manager.createTask('Test task', 'Test description');
      expect(task.title).toBe('Test task');
      expect(task.description).toBe('Test description');
      expect(task.completed).toBe(false);
      expect(task.id).toMatch(/^task-\d+$/);
    });

    it('should create a task with only title', () => {
      const task = manager.createTask('Title only');
      expect(task.title).toBe('Title only');
      expect(task.description).toBe('');
    });

    it('should trim whitespace from title and description', () => {
      const task = manager.createTask('  padded title  ', '  padded desc  ');
      expect(task.title).toBe('padded title');
      expect(task.description).toBe('padded desc');
    });

    it('should throw on empty title', () => {
      expect(() => manager.createTask('')).toThrow('Task title cannot be empty');
    });

    it('should throw on whitespace-only title', () => {
      expect(() => manager.createTask('   ')).toThrow('Task title cannot be empty');
    });

    it('should assign unique IDs', () => {
      const task1 = manager.createTask('Task 1');
      const task2 = manager.createTask('Task 2');
      expect(task1.id).not.toBe(task2.id);
    });
  });

  describe('getTask', () => {
    it('should return task by ID', () => {
      const created = manager.createTask('Find me');
      const found = manager.getTask(created.id);
      expect(found).toBeDefined();
      expect(found?.title).toBe('Find me');
    });

    it('should return undefined for non-existent ID', () => {
      expect(manager.getTask('task-999')).toBeUndefined();
    });
  });

  describe('getAllTasks', () => {
    it('should return empty array when no tasks', () => {
      expect(manager.getAllTasks()).toEqual([]);
    });

    it('should return all tasks', () => {
      manager.createTask('Task 1');
      manager.createTask('Task 2');
      manager.createTask('Task 3');
      expect(manager.getAllTasks()).toHaveLength(3);
    });
  });

  describe('updateTask', () => {
    it('should update title', () => {
      const task = manager.createTask('Original');
      const updated = manager.updateTask(task.id, 'Updated');
      expect(updated.title).toBe('Updated');
    });

    it('should update description', () => {
      const task = manager.createTask('Title', 'Old desc');
      const updated = manager.updateTask(task.id, undefined, 'New desc');
      expect(updated.description).toBe('New desc');
      expect(updated.title).toBe('Title');
    });

    it('should throw on non-existent task', () => {
      expect(() => manager.updateTask('task-999', 'New')).toThrow('Task not found');
    });

    it('should throw on empty title', () => {
      const task = manager.createTask('Original');
      expect(() => manager.updateTask(task.id, '')).toThrow('Task title cannot be empty');
    });
  });

  describe('completeTask', () => {
    it('should mark task as completed', () => {
      const task = manager.createTask('Complete me');
      const completed = manager.completeTask(task.id);
      expect(completed.completed).toBe(true);
    });

    it('should throw on non-existent task', () => {
      expect(() => manager.completeTask('task-999')).toThrow('Task not found');
    });
  });

  describe('deleteTask', () => {
    it('should delete an existing task', () => {
      const task = manager.createTask('Delete me');
      expect(manager.deleteTask(task.id)).toBe(true);
      expect(manager.getTask(task.id)).toBeUndefined();
    });

    it('should throw on non-existent task', () => {
      expect(() => manager.deleteTask('task-999')).toThrow('Task not found');
    });
  });

  describe('getStats', () => {
    it('should return zeros when empty', () => {
      expect(manager.getStats()).toEqual({ total: 0, completed: 0, pending: 0 });
    });

    it('should count completed and pending tasks', () => {
      const t1 = manager.createTask('Task 1');
      manager.createTask('Task 2');
      manager.createTask('Task 3');
      manager.completeTask(t1.id);

      expect(manager.getStats()).toEqual({ total: 3, completed: 1, pending: 2 });
    });
  });

  describe('searchTasks', () => {
    beforeEach(() => {
      manager.createTask('Set up CI/CD');
      manager.createTask('Write unit tests');
      manager.createTask('Set up monitoring');
    });

    it('should find tasks by partial title match', () => {
      const results = manager.searchTasks('set up');
      expect(results).toHaveLength(2);
    });

    it('should be case insensitive', () => {
      const results = manager.searchTasks('SET UP');
      expect(results).toHaveLength(2);
    });

    it('should return empty array for no matches', () => {
      const results = manager.searchTasks('nonexistent');
      expect(results).toHaveLength(0);
    });
  });

  describe('exportToJson / importFromJson', () => {
    it('should round-trip tasks through JSON', () => {
      manager.createTask('Task 1', 'Desc 1');
      manager.createTask('Task 2', 'Desc 2');

      const json = manager.exportToJson();
      const newManager = new TaskManager();
      const imported = newManager.importFromJson(json);

      expect(imported).toBe(2);
      expect(newManager.getAllTasks()).toHaveLength(2);
    });
  });
});
