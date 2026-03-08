from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class ScheduledEvent:
    id: str
    title: str
    date: datetime
    duration: int  # minutes


class EventScheduler:
    def __init__(self) -> None:
        self._events: List[ScheduledEvent] = []

    def add_event(self, event: ScheduledEvent) -> None:
        # Check for time conflicts
        for e in self._events:
            existing_end = e.date + timedelta(minutes=e.duration)
            new_end = event.date + timedelta(minutes=event.duration)
            if e.date < new_end and event.date < existing_end:
                raise ValueError(f"Time conflict with event: {e.title}")

        self._events.append(event)

    def remove_event(self, event_id: str) -> None:
        index = next(
            (i for i, e in enumerate(self._events) if e.id == event_id), -1
        )
        if index == -1:
            raise ValueError(f"Event not found: {event_id}")
        self._events.pop(index)

    # BUG: off-by-one error — uses < instead of <= for end date comparison
    # Events that fall exactly on the end date boundary are excluded
    def get_events_in_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[ScheduledEvent]:
        return [
            event
            for event in self._events
            if event.date >= start_date and event.date < end_date  # BUG: should be <=
        ]

    def get_event_by_id(self, event_id: str) -> Optional[ScheduledEvent]:
        return next(
            (e for e in self._events if e.id == event_id), None
        )

    def get_upcoming_events(
        self, from_date: datetime, count: int
    ) -> List[ScheduledEvent]:
        upcoming = [e for e in self._events if e.date >= from_date]
        upcoming.sort(key=lambda e: e.date)
        return upcoming[:count]

    def get_all_events(self) -> List[ScheduledEvent]:
        return list(self._events)
