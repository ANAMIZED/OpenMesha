from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = ConfigDict(env_prefix="OM_")

    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "info"
    data_dir: str = "data"
    llm_mode: str = "mock"  # mock | openai
    openai_api_key: str = ""

settings = Settings()
