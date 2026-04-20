from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )
    input_tokens_cost: float
    output_tokens_cost: float
    model: str
    api_key: str


settings = Settings()
