import aiofiles
import toml
import asyncio

from abc import ABC, abstractmethod
class Config(ABC):
    
    def __init__(self, config_path: str):
        self.config = None
        self.config_path = config_path
        
    async def load(self):
        self.config = await self._load_config(self.config_path)
        
    async def _load_config(self, config_path: str) -> dict:
        try:
            async with aiofiles.open(config_path, 'r', encoding='utf-8') as f:
                config_content = await f.read()
                return toml.loads(config_content)
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл конфига не найден: {config_path}')
        except toml.TomlDecodeError as e:
            raise ValueError(f'Произошла ошибка при декодировании: {e}')
        
    @abstractmethod
    def get(self, section: str, key: str, default=None):
        pass
    
class BotConfig(Config):
    
    def __init__(self, config_path: str):
        super().__init__(config_path)
        
    def get(self, section: str, key: str, default=None):
        try:
            return self.config[section][key]
        except KeyError:
            raise KeyError(f"Ключ '{key}' не найден в секции '{section}'")
        
    @property
    def telegram_bot_token(self) -> str:
        return self.get("TELEGRAM", "BOT_API_TOKEN")
    
    @property
    def newsapi_key(self) -> str:
        return self.get("NEWS", "NEWSAPI_KEY")
    
    @property
    def database_url(self) -> str:
        return self.get("DATABASE", "URL", "sqlite://db.sqlite3")
