from tortoise import Tortoise
from core.config.config import BotConfig

async def init_db(config: BotConfig):
    await Tortoise.init(
        db_url=config.database_url,
        modules={'models': ['core.database.models']}
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()