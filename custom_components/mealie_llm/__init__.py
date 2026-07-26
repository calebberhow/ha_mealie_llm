from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .llm import async_setup_llm


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    await async_setup_llm(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Mealie LLM from a config entry."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Mealie LLM config entry."""
    return True