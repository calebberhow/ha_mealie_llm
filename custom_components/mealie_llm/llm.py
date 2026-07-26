from homeassistant.core import HomeAssistant
from homeassistant.helpers import llm


DOMAIN = "mealie_llm"


class MealieRecipeTool(llm.Tool):
    """Tool for searching Mealie recipes."""

    name = "search_mealie_recipes"

    description = (
        "Search the household Mealie recipe database. "
        "Use this when the user asks to find or look up a recipe."
    )

    parameters = {
        "query": {
            "type": "string",
            "description": "Recipe name, ingredient, or search phrase"
        }
    }

    async def async_call(
        self,
        hass: HomeAssistant,
        tool_input: dict,
        conversation_id: str | None = None,
        context=None,
    ):
        query = tool_input["query"]

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

        return response

class MealieLLMAPI(llm.API):
    """Expose Mealie tools to Assist."""

    id = DOMAIN

    async def async_get_api_instance(
        self,
        hass: HomeAssistant,
        agent_id: str,
    ):
        return self

    async def async_get_tools(
        self,
        hass: HomeAssistant,
        api_instance,
    ):
        return [
            MealieRecipeTool()
        ]

async def async_setup_llm(hass: HomeAssistant):

    api = MealieLLMAPI()

    llm.async_register_api(
        hass,
        api,
    )