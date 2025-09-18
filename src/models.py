from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: int
    name: str
    email: str
    age: int
    city: str
    created_at: datetime = field(default_factory=datetime.now)

    def to_tuple(self) -> tuple:
        return (self.id, self.name, self.email, self.age, self.city, self.created_at)

    def __str__(self) -> str:
        return f"User({self.user_id}: {self.name}, {self.email}, {self.age}, {self.city}, {self.created_at})"
