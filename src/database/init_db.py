from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DataBaseConfig

config = DataBaseConfig()

engine = create_async_engine(config.db_uri, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
