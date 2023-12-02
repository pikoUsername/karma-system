from app.base.events.event import Event, event
from app.user.dto.user import UserDTO


@event
class UserCreated(Event):
    user: UserDTO


@event
class GivenSuperUser(Event):
    by: UserDTO
    user: UserDTO