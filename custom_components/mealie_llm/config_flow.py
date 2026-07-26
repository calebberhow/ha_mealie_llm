from homeassistant import config_entries
from homeassistant.core import callback


class MealieLLMConfigFlow(config_entries.ConfigFlow, domain="mealie_llm"):
    """Config flow for Mealie LLM."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup."""

        return self.async_create_entry(
            title="Mealie LLM",
            data={}
        )