from typing import cast

import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import llm
from homeassistant.util.json import JsonObjectType

DOMAIN = "mealie_llm"


class MealieRecipeTool(llm.Tool):
    """Tool for searching Mealie recipes."""

    name = "search_mealie_recipes"

    description = (
        "Search the household Mealie recipe database. "
        "Use this when the user asks to find or look up a recipe."
    )

    parameters = vol.Schema(
        {
            vol.Required(
                "query",
                description="Recipe name, ingredient, or search phrase",
            ): str,
        }
    )

    async def async_call(
        self,
        hass: HomeAssistant,
        tool_input: llm.ToolInput,
        llm_context: llm.LLMContext
    ) -> JsonObjectType:
        data = cast(dict[str, str], self.parameters(tool_input.tool_args))
        query = data["query"]

        entries = hass.config_entries.async_entries("mealie")

        if not entries:
            return {
                "error": "No Mealie integration configured"
            }

        mealie_entry = entries[0]

        response = await hass.services.async_call(
            "mealie",
            "get_recipes",
            {
                "config_entry_id": mealie_entry.entry_id,
                "search_terms": query,
                "result_limit": 5,
            },
            blocking=True,
            return_response=True,
        )

        if response is None:
            return {"error": "Mealie returned no response"}

        return cast(JsonObjectType, response)

class MealieLLMAPI(llm.API):
    """Expose Mealie tools to Assist."""

    id = DOMAIN

    async def async_get_api_instance(
        self,
        llm_context: llm.LLMContext
    ) -> llm.APIInstance:
        return llm.APIInstance(self, "Always use these tools to search the household Mealie recipe database when the user asks to find or look up a recipe.", llm_context, [MealieRecipeTool()])

async def async_setup_llm(hass: HomeAssistant):
    """Register the Mealie LLM API with Home Assistant."""
    if any(api.id == DOMAIN for api in llm.async_get_apis(hass)):
        return

    api = MealieLLMAPI(hass=hass, id=DOMAIN, name="Mealie Recipes")

    llm.async_register_api(
        hass,
        api,
    )