from typing import Any

from fastapi import APIRouter, Body, HTTPException
from fastapi.security import HTTPBearer

from fastlibrarian.config import AppConfig, config_manager, get_config

router = APIRouter(prefix="/config", tags=["configuration"])
security = HTTPBearer(auto_error=False)


@router.get("/", response_model=dict[str, Any])
async def get_current_config() -> dict[str, Any]:
    """Get the current configuration with sensitive values masked."""
    config = get_config()
    return config.get_masked_dict()


@router.get("/raw")
async def get_raw_config() -> dict[str, str]:
    """Get the raw TOML configuration as string."""
    try:
        config = get_config()
        toml_string = config_manager.save_config_as_string(config)
        return {"toml": toml_string}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to serialize config: {e!s}",
        )


@router.get("/schema", response_model=dict[str, Any])
async def get_config_schema() -> dict[str, Any]:
    """Get the configuration schema for validation and UI generation."""
    return AppConfig.model_json_schema()


@router.put("/")
async def update_config(config_update: dict[str, Any]) -> dict[str, str]:
    """Update configuration and save to file."""
    try:
        # Validate by creating a new config instance
        current_config = get_config()
        updated_data = current_config.model_dump()

        # Deep merge the updates
        def deep_update(base_dict: dict, update_dict: dict) -> dict:
            for key, value in update_dict.items():
                if (
                    key in base_dict
                    and isinstance(base_dict[key], dict)
                    and isinstance(value, dict)
                ):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value
            return base_dict

        updated_data = deep_update(updated_data, config_update)

        # Create new config to validate
        new_config = AppConfig(**updated_data)

        # Save the configuration
        config_manager.save_config(new_config)
        config_manager._config = new_config

        return {"message": "Configuration updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid configuration: {e!s}")


@router.put("/raw")
async def update_config_from_toml(
    toml_content: str = Body(..., embed=True, description="Raw TOML configuration"),
) -> dict[str, str]:
    """Update configuration from raw TOML string."""
    try:
        # First validate the TOML syntax
        is_valid, error_msg = config_manager.validate_toml_string(toml_content)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid TOML syntax: {error_msg}",
            )

        # Load and validate the configuration
        new_config = config_manager.load_config_from_string(toml_content)

        # Save to file
        config_manager.save_config(new_config)

        return {"message": "Configuration updated from TOML string successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update configuration: {e!s}",
        )


@router.post("/validate")
async def validate_config_toml(
    toml_content: str = Body(
        ...,
        embed=True,
        description="TOML configuration to validate",
    ),
) -> dict[str, Any]:
    """Validate TOML configuration without saving."""
    try:
        # Validate TOML syntax
        is_valid_toml, toml_error = config_manager.validate_toml_string(toml_content)
        if not is_valid_toml:
            return {
                "valid": False,
                "toml_valid": False,
                "config_valid": False,
                "errors": [f"TOML syntax error: {toml_error}"],
            }

        # Validate configuration structure
        try:
            temp_config = config_manager.load_config_from_string(toml_content)
            return {
                "valid": True,
                "toml_valid": True,
                "config_valid": True,
                "errors": [],
            }
        except Exception as config_error:
            return {
                "valid": False,
                "toml_valid": True,
                "config_valid": False,
                "errors": [f"Configuration validation error: {config_error!s}"],
            }

    except Exception as e:
        return {
            "valid": False,
            "toml_valid": False,
            "config_valid": False,
            "errors": [f"Validation error: {e!s}"],
        }


@router.post("/reload")
async def reload_config() -> dict[str, str]:
    """Reload configuration from file and environment variables."""
    try:
        config_manager.load_config(force_reload=True)
        return {"message": "Configuration reloaded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reload configuration: {e!s}",
        )


@router.get("/validate-file")
async def validate_config_file() -> dict[str, Any]:
    """Validate the current configuration file."""
    try:
        is_valid, message = config_manager.validate_toml_file()
        return {
            "valid": is_valid,
            "message": message,
            "file_path": str(config_manager.config_path),
        }
    except Exception as e:
        return {
            "valid": False,
            "message": f"Validation error: {e!s}",
            "file_path": str(config_manager.config_path),
        }


@router.get("/health")
async def config_health_check() -> dict[str, Any]:
    """Health check endpoint that validates current configuration."""
    try:
        config = get_config()
        return {
            "status": "healthy",
            "environment": config.environment,
            "version": config.api.version,
            "database_configured": bool(config.database.url),
            "external_apis_configured": bool(config.external_apis.hardcover_api_key),
            "toml_parser": "rtoml",
            "config_file_exists": config_manager.config_path.exists(),
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "toml_parser": "rtoml",
        }
