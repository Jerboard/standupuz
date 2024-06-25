from datetime import datetime, date, time
import typing as t
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_postgresql
from utilits.entities_utils import save_entities
from utilits.text_utils import add_tags

from .base import METADATA, begin_connection
from config import Config
from .sqlite_temp import get_events, get_entities


class EventRow(t.Protocol):
    id: int
    created_at: datetime
    title: str
    event_date: date
    event_time: time
    text: str
    photo_id: str
    is_active: bool
    page_id: int
    text_1: str
    text_2: str
    text_3: str
    text_site: str


EventTable: sa.Table = sa.Table(
    "events",
    METADATA,

    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('created_at', sa.DateTime(timezone=True)),
    sa.Column('title', sa.String(255)),
    sa.Column('event_date', sa.Date()),
    sa.Column('event_time', sa.Time()),
    sa.Column('text', sa.Text()),
    sa.Column('entities', sa_postgresql.ARRAY(sa.String(255))),
    sa.Column('photo_id', sa.String(255)),
    sa.Column('is_active', sa.Boolean()),
    sa.Column('page_id', sa.Integer),
    sa.Column('text_1', sa.Text()),
    sa.Column('text_2', sa.Text()),
    sa.Column('text_3', sa.Text()),
    # sa.Column('text_site', sa.Text()),
)


async def add_event(
        title: str,
        event_date: date,
        event_time: time,
        text: str,
        entities: list[str],
        photo_id: str,
        is_active: bool,
        page_id: int,
        text_1: str,
        text_2: str,
        text_3: str,
        # text_site: str

) -> None:
    now = datetime.now(Config.tz)
    query = EventTable.insert().values(
        created_at=now,
        title=title,
        event_date=event_date,
        event_time=event_time,
        text=text,
        entities=entities,
        photo_id=photo_id,
        is_active=is_active,
        page_id=page_id,
        text_1=text_1,
        text_2=text_2,
        text_3=text_3,
        # text_site=text_site,
    )
    async with begin_connection() as conn:
        await conn.execute(query)


async def add_events():
    time_start = datetime.now()
    events = get_events()
    for event in events[-5:]:
        event_entities = save_entities(get_entities(event[0]))
        # text_site = add_tags(event[5], get_entities(event[0]))
        # print(text_site)
        # dt = datetime.strptime(event[3], '%d.%m').replace(year=2024)

        # await add_event(
        #     title=event[2],
        #     event_date=datetime.strptime(event[3], '%d.%m').replace(year=2024).date(),
        #     event_time=datetime.strptime(event[4], '%H:%M').time(),
        #     text=event[5],
        #     entities=event_entities,
        #     photo_id=event[6],
        #     is_active=True,
        #     page_id=event[8],
        #     text_1=event[9],
        #     text_2=event[10],
        #     text_3=event[11],
        # )

    print(datetime.now() - time_start)
'''
CREATE TABLE events (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    add_time   TEXT,
    title      TEXT,
    event_date TEXT,
    event_time TEXT,
    text       TEXT,
    photo_id   TEXT,
    is_active  INTEGER DEFAULT (0),
    page_id    INTEGER,
    text_1     TEXT,
    text_2     TEXT,
    text_3     TEXT
);

'''