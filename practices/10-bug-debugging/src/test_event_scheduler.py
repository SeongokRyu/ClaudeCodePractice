import pytest
from datetime import datetime
from event_scheduler import EventScheduler, ScheduledEvent


class TestEventSchedulerAddEvent:
    def setup_method(self):
        self.scheduler = EventScheduler()

    def test_should_add_a_new_event(self):
        event = ScheduledEvent(
            id="1",
            title="Meeting",
            date=datetime(2024, 3, 15, 10, 0, 0),
            duration=60,
        )
        self.scheduler.add_event(event)
        assert len(self.scheduler.get_all_events()) == 1

    def test_should_throw_on_time_conflict(self):
        self.scheduler.add_event(
            ScheduledEvent(
                id="1",
                title="Meeting 1",
                date=datetime(2024, 3, 15, 10, 0, 0),
                duration=60,
            )
        )
        with pytest.raises(ValueError, match="Time conflict"):
            self.scheduler.add_event(
                ScheduledEvent(
                    id="2",
                    title="Meeting 2",
                    date=datetime(2024, 3, 15, 10, 30, 0),
                    duration=60,
                )
            )


class TestEventSchedulerGetEventsInRange:
    def setup_method(self):
        self.scheduler = EventScheduler()
        self.scheduler.add_event(
            ScheduledEvent(
                id="1",
                title="March 1st Event",
                date=datetime(2024, 3, 1, 10, 0, 0),
                duration=60,
            )
        )
        self.scheduler.add_event(
            ScheduledEvent(
                id="2",
                title="March 15th Event",
                date=datetime(2024, 3, 15, 10, 0, 0),
                duration=60,
            )
        )
        self.scheduler.add_event(
            ScheduledEvent(
                id="3",
                title="March 31st Event",
                date=datetime(2024, 3, 31, 10, 0, 0),
                duration=60,
            )
        )
        self.scheduler.add_event(
            ScheduledEvent(
                id="4",
                title="April 5th Event",
                date=datetime(2024, 4, 5, 10, 0, 0),
                duration=60,
            )
        )

    def test_should_return_events_within_range(self):
        events = self.scheduler.get_events_in_range(
            datetime(2024, 3, 10, 0, 0, 0),
            datetime(2024, 3, 20, 0, 0, 0),
        )
        assert len(events) == 1
        assert events[0].title == "March 15th Event"

    def test_should_include_events_on_the_start_date(self):
        events = self.scheduler.get_events_in_range(
            datetime(2024, 3, 1, 10, 0, 0),
            datetime(2024, 3, 20, 0, 0, 0),
        )
        assert len(events) == 2

    # This test FAILS due to the off-by-one bug
    def test_should_include_events_on_the_end_date_boundary(self):
        events = self.scheduler.get_events_in_range(
            datetime(2024, 3, 1, 0, 0, 0),
            datetime(2024, 3, 31, 10, 0, 0),  # exactly matches March 31st event time
        )
        # BUG: The implementation uses < instead of <=, so the March 31st event is excluded
        assert len(events) == 3

    def test_should_return_empty_list_when_no_events_in_range(self):
        events = self.scheduler.get_events_in_range(
            datetime(2024, 5, 1, 0, 0, 0),
            datetime(2024, 5, 31, 0, 0, 0),
        )
        assert len(events) == 0


class TestEventSchedulerGetUpcomingEvents:
    def setup_method(self):
        self.scheduler = EventScheduler()

    def test_should_return_events_sorted_by_date(self):
        self.scheduler.add_event(
            ScheduledEvent(
                id="1",
                title="Later",
                date=datetime(2024, 3, 20, 10, 0, 0),
                duration=60,
            )
        )
        self.scheduler.add_event(
            ScheduledEvent(
                id="2",
                title="Sooner",
                date=datetime(2024, 3, 10, 10, 0, 0),
                duration=60,
            )
        )

        upcoming = self.scheduler.get_upcoming_events(
            datetime(2024, 3, 1, 0, 0, 0), 5
        )
        assert upcoming[0].title == "Sooner"
        assert upcoming[1].title == "Later"
