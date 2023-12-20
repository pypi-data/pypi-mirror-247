from typing import Any, Optional

from oryks_google_oauth import GoogleCalendarScopes, GoogleOAuth
from pydantic import BaseModel, Field

from .models import Event
from .resources import EventResource


class GoogleCalendar(BaseModel):
    secret_file: Optional[str] = None
    api_service_name: Optional[str] = "calendar"
    api_version: Optional[str] = "v3"
    credentials_dir: Optional[str] = ".calendar"
    scopes: Optional[list[str]] = Field(
        default=[
            GoogleCalendarScopes.calendar.value,
            GoogleCalendarScopes.calendar_events.value,
            GoogleCalendarScopes.calendar_settings_readonly.value,
        ]
    )
    calendar_client: Optional[Any] = None

    def authenticate(self, secret_file: Optional[str] = None) -> None:
        if secret_file:
            self.secret_file = secret_file
        if not self.secret_file:
            raise ValueError("The secret file was not provided.")
        oauth: GoogleOAuth = GoogleOAuth(
            secrets_file=self.secret_file,
            scopes=self.scopes,
            api_service_name=self.api_service_name,
            api_version=self.api_version,
            credentials_dir=self.credentials_dir,
        )
        self.calendar_client = oauth.authenticate_google_server()

    def create_event(self) -> Event:
        event_resource: EventResource = EventResource(
            calendar_client=self.calendar_client
        )
        return event_resource.create_event()

    def get_event(self) -> Event:
        event_resource: EventResource = EventResource(
            calendar_client=self.calendar_client
        )
        return event_resource.get_event()

    def delete_event(self) -> None:
        event_resource: EventResource = EventResource(
            calendar_client=self.calendar_client
        )
        return event_resource.delete_event()
