from pydantic_settings import BaseSettings, SettingsConfigDict 
    
class Settings(BaseSettings):
    '''the application configuration'''    
    TITLE: str = 'Helios API'
    VERSION: str = '0.1'
    DESCRIPTION: str = 'the backend for the Helios platform.'
    
    LOG_TO_CONSOLE: bool = True
    LOG_TO_FILE: bool = True
    
    SECRET_KEY: str 
    DATABASE_URL: str
    DEBUG: bool = True 
    DB_ECHO: bool = True 
    
    model_config = SettingsConfigDict(
        env_file=".env",
        frozen=True,
        extra="ignore"
    )

settings = Settings() # type: ignore 
