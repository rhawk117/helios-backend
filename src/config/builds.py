from pydantic_settings import BaseSettings, SettingsConfigDict 

    
class Settings(BaseSettings):
    '''the application configuration'''    
    TITLE: str = 'Helios API'
    VERSION: str = '0.1'
    DESCRIPTION: str = 'the backend for the Helios platform.'
    
    
    SECRET_KEY: str 
    DATABASE_URL: str
    DEBUG: bool = True 
    
    model_config = SettingsConfigDict(
        env_file=".env",
        frozen=True,
        extra="ignore"
    )

settings = Settings() # type: ignore 