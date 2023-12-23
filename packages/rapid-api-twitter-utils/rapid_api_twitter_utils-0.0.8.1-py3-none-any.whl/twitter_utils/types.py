import datetime
from dataclasses import dataclass


@dataclass
class UserObject:
    id: str
    name: str
    screen_name: str

    img: str
    banner: str
    description: str
    location: str

    favourites_count: str
    followers_count: str
    following_count: str

    tweets_count: int
    account_age: datetime.datetime
