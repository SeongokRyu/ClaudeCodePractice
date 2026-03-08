export interface ScheduledEvent {
  id: string;
  title: string;
  date: Date;
  duration: number; // minutes
}

export class EventScheduler {
  private events: ScheduledEvent[] = [];

  addEvent(event: ScheduledEvent): void {
    // Check for time conflicts
    const conflict = this.events.find((e) => {
      const existingEnd = new Date(e.date.getTime() + e.duration * 60000);
      const newEnd = new Date(event.date.getTime() + event.duration * 60000);
      return e.date < newEnd && event.date < existingEnd;
    });

    if (conflict) {
      throw new Error(`Time conflict with event: ${conflict.title}`);
    }

    this.events.push(event);
  }

  removeEvent(eventId: string): void {
    const index = this.events.findIndex((e) => e.id === eventId);
    if (index === -1) {
      throw new Error(`Event not found: ${eventId}`);
    }
    this.events.splice(index, 1);
  }

  // BUG: off-by-one error — uses < instead of <= for end date comparison
  // Events that fall exactly on the end date boundary are excluded
  getEventsInRange(startDate: Date, endDate: Date): ScheduledEvent[] {
    return this.events.filter((event) => {
      return event.date >= startDate && event.date < endDate;  // BUG: should be <=
    });
  }

  getEventById(eventId: string): ScheduledEvent | undefined {
    return this.events.find((e) => e.id === eventId);
  }

  getUpcomingEvents(fromDate: Date, count: number): ScheduledEvent[] {
    return this.events
      .filter((e) => e.date >= fromDate)
      .sort((a, b) => a.date.getTime() - b.date.getTime())
      .slice(0, count);
  }

  getAllEvents(): ScheduledEvent[] {
    return [...this.events];
  }
}
