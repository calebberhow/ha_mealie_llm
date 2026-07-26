from homeassistant.core import HomeAssistant

from .llm import async_setup_llm


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    await async_setup_llm(hass)
    return True