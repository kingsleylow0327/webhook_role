import os

from dotenv import load_dotenv

class Config():
    
    def __init__(self) -> None:
        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        self.DB_ADDRESS = os.getenv('DB_ADDRESS')
        self.DB_SCHEMA = os.getenv('DB_SCHEMA')
        self.DB_USERNAME = os.getenv('DB_USERNAME')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_PORT = os.getenv('DB_PORT')
        self.POOL_SIZE = os.getenv('POOL_SIZE')