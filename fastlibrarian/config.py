from functools import cached_property
from pathlib import Path
from typing import Any

import rtoml
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    """Database configuration section."""

    user: str = Field(default="fastlib", min_length=1)
    password: str = Field(default="fastpassword", min_length=8)
    host: str = Field(default="localhost", min_length=1)
    port: int = Field(default=5432, ge=1024, le=65535)
    database: str = Field(default="fastlibrarian", min_length=1)
    url: str = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    echo: bool = True
    pool_size: int = Field(default=10, ge=1, le=100)
    max_overflow: int = Field(default=20, ge=0, le=50)

    model_config = ConfigDict(extra="forbid")


class APIConfig(BaseModel):
    """API configuration section."""

    title: str = "FastLibrarian API"
    version: str = "1.0.0"
    description: str = "A fast and efficient librarian API"
    debug: bool = False
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1024, le=65535)

    model_config = ConfigDict(extra="forbid")


class ExternalAPIConfig(BaseModel):
    """External API configuration section."""

    hardcover_api_key: str = Field(default="", description="Hardcover API key")
    inventaire_enabled: bool = False
    rate_limit_requests: int = Field(default=100, ge=1)
    rate_limit_window: int = Field(default=3600, ge=1)  # seconds
    timeout: float = Field(default=30.0, ge=1.0)

    model_config = ConfigDict(extra="forbid")

    @field_validator("hardcover_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate API key format if provided."""
        if v and len(v) < 10:
            logger.warning("API key seems too short, please verify")
        return v


class LoggingConfig(BaseModel):
    """Logging configuration section."""

    level: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    format: str = "{time} | {level} | {message}"
    rotation: str = "10 MB"
    retention: str = "7 days"
    file_path: str | None = None

    model_config = ConfigDict(extra="forbid")


class SecurityConfig(BaseModel):
    """Security configuration section."""

    secret_key: str = Field(default="", min_length=32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=30, ge=1)

    model_config = ConfigDict(extra="forbid")


class AppConfig(BaseSettings):
    """Main application configuration using Pydantic Settings."""

    # App metadata
    app_name: str = "FastLibrarian"
    environment: str = Field(
        default="development",
        pattern="^(development|staging|production)$",
    )

    # Configuration sections
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    external_apis: ExternalAPIConfig = Field(default_factory=ExternalAPIConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",  # Allows DATABASE__URL format
        case_sensitive=False,
        extra="forbid",
        validate_assignment=True,
    )

    @computed_field
    @cached_property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @computed_field
    @cached_property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"

    # Legacy compatibility properties
    @property
    def hc_api_key(self) -> str:
        """Legacy property for backward compatibility."""
        return self.external_apis.hardcover_api_key

    @property
    def version(self) -> str:
        """App version from API config."""
        return self.api.version

    @property
    def description(self) -> str:
        """App description from API config."""
        return self.api.description

    def get_masked_dict(self) -> dict[str, Any]:
        """Get configuration as dict with sensitive values masked."""
        config_dict = self.model_dump()

        # Mask sensitive values
        sensitive_fields = [
            ("database", "url"),
            ("external_apis", "hardcover_api_key"),
            ("security", "secret_key"),
        ]

        for section, field in sensitive_fields:
            if section in config_dict and field in config_dict[section]:
                value = config_dict[section][field]
                if value and isinstance(value, str) and len(value) > 8:
                    config_dict[section][field] = (
                        f"{value[:4]}{'*' * (len(value) - 8)}{value[-4:]}"
                    )

        return config_dict


class ConfigManager:
    """Configuration manager with TOML file support using rtoml for performance."""

    def __init__(self, config_path: Path | None = None, env_file: Path | None = None):
        self.config_path = config_path or Path("config.toml")
        self.env_file = env_file or Path(".env")
        self._config: AppConfig | None = None
        self._file_mtime: float | None = None

    def load_config(self, force_reload: bool = False) -> AppConfig:
        """Load configuration with hot reloading support using rtoml."""
        # Check if we need to reload
        if not force_reload and self._config is not None:
            if self.config_path.exists():
                current_mtime = self.config_path.stat().st_mtime
                if self._file_mtime == current_mtime:
                    return self._config
            else:
                return self._config

        # Load TOML configuration using rtoml
        toml_config = {}
        if self.config_path.exists():
            try:
                toml_config = rtoml.load(self.config_path)
                self._file_mtime = self.config_path.stat().st_mtime
                logger.info(f"Loaded configuration from {self.config_path} using rtoml")
            except Exception as e:
                logger.error(f"Failed to load TOML config with rtoml: {e}")

        # Create configuration with TOML overrides
        try:
            # Override environment file if specified
            if self.env_file.exists():
                self._config = AppConfig(_env_file=str(self.env_file), **toml_config)
            else:
                self._config = AppConfig(**toml_config)

            logger.success("Configuration loaded successfully")
            return self._config

        except Exception as e:
            logger.error(f"Failed to create configuration: {e}")
            # Return default config if loading fails
            self._config = AppConfig()
            return self._config

    def save_config(self, config: AppConfig | None = None) -> None:
        """Save configuration to TOML file using rtoml."""
        if config is None:
            config = self._config

        if config is None:
            raise ValueError("No configuration to save")

        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # Convert to dict and save using rtoml
            config_dict = config.model_dump(exclude={"app_name", "environment"})

            # rtoml.dump expects a file path, not a file object
            rtoml.dump(config_dict, self.config_path)

            self._file_mtime = self.config_path.stat().st_mtime
            logger.success(f"Configuration saved to {self.config_path} using rtoml")

        except Exception as e:
            logger.error(f"Failed to save configuration with rtoml: {e}")
            raise

    def save_config_as_string(self, config: AppConfig | None = None) -> str:
        """Save configuration as TOML string using rtoml."""
        if config is None:
            config = self._config

        if config is None:
            raise ValueError("No configuration to save")

        try:
            config_dict = config.model_dump(exclude={"app_name", "environment"})
            return rtoml.dumps(config_dict)
        except Exception as e:
            logger.error(f"Failed to serialize configuration with rtoml: {e}")
            raise

    def load_config_from_string(self, toml_string: str) -> AppConfig:
        """Load configuration from TOML string using rtoml."""
        try:
            toml_config = rtoml.loads(toml_string)

            # Create configuration with TOML data
            if self.env_file.exists():
                self._config = AppConfig(_env_file=str(self.env_file), **toml_config)
            else:
                self._config = AppConfig(**toml_config)

            logger.success("Configuration loaded from string successfully")
            return self._config

        except Exception as e:
            logger.error(f"Failed to load configuration from string: {e}")
            raise

    def reload_if_changed(self) -> AppConfig:
        """Reload configuration if file has changed."""
        return self.load_config(force_reload=False)

    def validate_toml_file(self, file_path: Path | None = None) -> tuple[bool, str]:
        """Validate TOML file syntax without loading into config."""
        path = file_path or self.config_path
        try:
            if not path.exists():
                return False, f"File {path} does not exist"

            rtoml.load(path)
            return True, "TOML file is valid"
        except Exception as e:
            return False, f"Invalid TOML: {e!s}"

    def validate_toml_string(self, toml_string: str) -> tuple[bool, str]:
        """Validate TOML string syntax."""
        try:
            rtoml.loads(toml_string)
            return True, "TOML string is valid"
        except Exception as e:
            return False, f"Invalid TOML: {e!s}"

    @property
    def config(self) -> AppConfig:
        """Get current configuration, loading if necessary."""
        if self._config is None:
            return self.load_config()
        return self.reload_if_changed()


# Global instances
config_manager = ConfigManager()


def get_config() -> AppConfig:
    """Get the current configuration."""
    return config_manager.config


def get_settings() -> AppConfig:
    """Alternative function name for FastAPI dependency injection."""
    return config_manager.config
