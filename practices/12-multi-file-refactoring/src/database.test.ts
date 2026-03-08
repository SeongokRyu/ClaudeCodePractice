import * as db from './database';

describe('Database', () => {
  beforeEach((done) => {
    db.clearAll(() => {
      db.initCollection('test', (error) => {
        if (error) return done(error);
        done();
      });
    });
  });

  describe('insert', () => {
    it('should insert a document', (done) => {
      db.insert('test', '1', { name: 'Alice' }, (error, result) => {
        expect(error).toBeNull();
        expect(result).toEqual({ name: 'Alice' });
        done();
      });
    });

    it('should reject duplicate IDs', (done) => {
      db.insert('test', '1', { name: 'Alice' }, (error) => {
        expect(error).toBeNull();
        db.insert('test', '1', { name: 'Bob' }, (error2) => {
          expect(error2).not.toBeNull();
          expect(error2!.message).toContain('already exists');
          done();
        });
      });
    });

    it('should reject insert to non-existent collection', (done) => {
      db.insert('nonexistent', '1', { name: 'Alice' }, (error) => {
        expect(error).not.toBeNull();
        expect(error!.message).toContain('does not exist');
        done();
      });
    });
  });

  describe('findById', () => {
    it('should find a document by ID', (done) => {
      db.insert('test', '1', { name: 'Alice' }, () => {
        db.findById('test', '1', (error, result) => {
          expect(error).toBeNull();
          expect(result).toEqual({ name: 'Alice' });
          done();
        });
      });
    });

    it('should return error for non-existent document', (done) => {
      db.findById('test', 'nonexistent', (error) => {
        expect(error).not.toBeNull();
        expect(error!.message).toContain('not found');
        done();
      });
    });
  });

  describe('findAll', () => {
    it('should return all documents', (done) => {
      db.insert('test', '1', { name: 'Alice' }, () => {
        db.insert('test', '2', { name: 'Bob' }, () => {
          db.findAll('test', (error, results) => {
            expect(error).toBeNull();
            expect(results).toHaveLength(2);
            done();
          });
        });
      });
    });
  });

  describe('update', () => {
    it('should update a document', (done) => {
      db.insert('test', '1', { name: 'Alice', age: 25 }, () => {
        db.update('test', '1', { age: 26 }, (error, result) => {
          expect(error).toBeNull();
          expect(result).toEqual({ name: 'Alice', age: 26 });
          done();
        });
      });
    });

    it('should return error for non-existent document', (done) => {
      db.update('test', 'nonexistent', { name: 'New' }, (error) => {
        expect(error).not.toBeNull();
        done();
      });
    });
  });

  describe('remove', () => {
    it('should remove a document', (done) => {
      db.insert('test', '1', { name: 'Alice' }, () => {
        db.remove('test', '1', (error) => {
          expect(error).toBeNull();
          db.findById('test', '1', (error2) => {
            expect(error2).not.toBeNull();
            done();
          });
        });
      });
    });
  });
});
