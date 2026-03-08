import { EventScheduler, ScheduledEvent } from './event-scheduler';

describe('EventScheduler', () => {
  let scheduler: EventScheduler;

  beforeEach(() => {
    scheduler = new EventScheduler();
  });

  describe('addEvent', () => {
    it('should add a new event', () => {
      const event: ScheduledEvent = {
        id: '1',
        title: 'Meeting',
        date: new Date('2024-03-15T10:00:00'),
        duration: 60,
      };
      scheduler.addEvent(event);
      expect(scheduler.getAllEvents()).toHaveLength(1);
    });

    it('should throw on time conflict', () => {
      scheduler.addEvent({
        id: '1',
        title: 'Meeting 1',
        date: new Date('2024-03-15T10:00:00'),
        duration: 60,
      });
      expect(() => {
        scheduler.addEvent({
          id: '2',
          title: 'Meeting 2',
          date: new Date('2024-03-15T10:30:00'),
          duration: 60,
        });
      }).toThrow('Time conflict');
    });
  });

  describe('getEventsInRange', () => {
    beforeEach(() => {
      scheduler.addEvent({
        id: '1',
        title: 'March 1st Event',
        date: new Date('2024-03-01T10:00:00'),
        duration: 60,
      });
      scheduler.addEvent({
        id: '2',
        title: 'March 15th Event',
        date: new Date('2024-03-15T10:00:00'),
        duration: 60,
      });
      scheduler.addEvent({
        id: '3',
        title: 'March 31st Event',
        date: new Date('2024-03-31T10:00:00'),
        duration: 60,
      });
      scheduler.addEvent({
        id: '4',
        title: 'April 5th Event',
        date: new Date('2024-04-05T10:00:00'),
        duration: 60,
      });
    });

    it('should return events within range', () => {
      const events = scheduler.getEventsInRange(
        new Date('2024-03-10T00:00:00'),
        new Date('2024-03-20T00:00:00')
      );
      expect(events).toHaveLength(1);
      expect(events[0].title).toBe('March 15th Event');
    });

    it('should include events on the start date', () => {
      const events = scheduler.getEventsInRange(
        new Date('2024-03-01T10:00:00'),
        new Date('2024-03-20T00:00:00')
      );
      expect(events).toHaveLength(2);
    });

    // This test FAILS due to the off-by-one bug
    it('should include events on the end date boundary', () => {
      const events = scheduler.getEventsInRange(
        new Date('2024-03-01T00:00:00'),
        new Date('2024-03-31T10:00:00')  // exactly matches March 31st event time
      );
      // BUG: The implementation uses < instead of <=, so the March 31st event is excluded
      expect(events).toHaveLength(3);
    });

    it('should return empty array when no events in range', () => {
      const events = scheduler.getEventsInRange(
        new Date('2024-05-01T00:00:00'),
        new Date('2024-05-31T00:00:00')
      );
      expect(events).toHaveLength(0);
    });
  });

  describe('getUpcomingEvents', () => {
    it('should return events sorted by date', () => {
      scheduler.addEvent({
        id: '1',
        title: 'Later',
        date: new Date('2024-03-20T10:00:00'),
        duration: 60,
      });
      scheduler.addEvent({
        id: '2',
        title: 'Sooner',
        date: new Date('2024-03-10T10:00:00'),
        duration: 60,
      });

      const upcoming = scheduler.getUpcomingEvents(
        new Date('2024-03-01T00:00:00'),
        5
      );
      expect(upcoming[0].title).toBe('Sooner');
      expect(upcoming[1].title).toBe('Later');
    });
  });
});
