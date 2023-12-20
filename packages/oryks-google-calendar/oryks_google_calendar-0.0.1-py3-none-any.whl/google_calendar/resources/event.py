from ..models import Event
from .calendar_resource import CalendarResource


class EventResource(CalendarResource):
    def create_event(self) -> Event:
        event = {
            "summary": "Google I/O 2015",
            "location": "800 Howard St., San Francisco, CA 94103",
            "description": "A chance to hear more about Google's developer products.",
            "start": {
                "dateTime": "2015-05-28T09:00:00-07:00",
                "timeZone": "America/Los_Angeles",
            },
            "end": {
                "dateTime": "2015-05-28T17:00:00-07:00",
                "timeZone": "America/Los_Angeles",
            },
            "recurrence": ["RRULE:FREQ=DAILY;COUNT=2"],
            "attendees": [
                {"email": "lpage@example.com"},
                {"email": "sbrin@example.com"},
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }

        event = (
            self.calendar_client.events()
            .insert(calendarId="primary", body=event)
            .execute()
        )
        return event

    def get_event(self) -> Event:
        event = (
            self.calendar_client.events()
            .get(calendarId="primary", eventId="4b1c4bof7ia3r5klrh4q83qsm8")
            .execute()
        )
        return event

    def delete_event(self) -> None:
        self.calendar_client.events().delete(
            calendarId="primary", eventId="eventId"
        ).execute()
