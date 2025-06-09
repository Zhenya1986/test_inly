from databases import Database

import settings

_global: dict[str, Database] = {}
DATABASE_URL = f"postgresql+asyncpg://{settings.BD_USER}:{settings.BD_PASSWORD}@{settings.BD_HOST}:{settings.BD_PORT}/{settings.BD_NAME}"

class DBInitError(Exception): ...


async def init_db():
    _global["db"] = Database(DATABASE_URL)
    await _global["db"].connect()


async def close_db():
    await _global["db"].disconnect()


def get_db():
    if not _global.get("db"):
        raise DBInitError()
    return _global["db"]
