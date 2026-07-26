from typing import cast

import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import llm
from homeassistant.util.json import JsonObjectType

DOMAIN = "mealie_llm"


class MealieRecipeSearchTool(llm.Tool):
    """Tool for searching Mealie recipes."""

    name = "search_mealie_recipes"

    description = (
        "Search the household Mealie recipe database for a list of recipes. "
        "Use this when the user asks to find or look up multiple recipes. "
        "Returns a short list of recipes matching the search phrase."
    )

    parameters = vol.Schema(
        {
            vol.Required(
                "query",
                description="Recipe name or search phrase",
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

class MealieRecipeDetailsTool(llm.Tool):
    """Tool for searching details about a single Mealie recipe."""

    name = "search_mealie_recipe_details"

    description = (
        "Search the household Mealie recipe database for a single recipe. "
        "Use this when the user asks to find or look up details about a specific recipe. "
        "Do not use when the user asks to add a recipe to a meal plan. "
        "Returns detailed information about the recipe including a full list of ingredients and instructions."
    )

    parameters = vol.Schema(
        {
            vol.Required(
                "query",
                description="Recipe name or search phrase",
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
                "result_limit": 1,
            },
            blocking=True,
            return_response=True,
        )

        if response is None:
            return {"error": "Mealie returned no response"}
        result = cast(dict[str, object], response)

        recipes = result.get("recipes")
        if not isinstance(recipes, dict):
            return {"error": "Unexpected response format. Recipes is not a property of the response."}

        items = recipes.get("items")
        if not isinstance(items, list) or not items:
            return {"error": "No recipes found. Items is not a property of the recipes."}

        first_recipe = items[0]
        if not isinstance(first_recipe, dict):
            return {"error": "Unexpected recipe item format. First recipe is not a dictionary."}

        slug = first_recipe.get("slug")
        if not isinstance(slug, str):
            return {"error": "Unexpected recipe item format. Slug is not a string."}

        response = await hass.services.async_call(
            "mealie",
            "get_recipe",
            {
                "config_entry_id": mealie_entry.entry_id,
                "recipe_id": slug,
            },
            blocking=True,
            return_response=True,
        )

        return cast(JsonObjectType, response)

class MealieMealplanSearchTool(llm.Tool):
    """Tool for searching Mealie meal plans."""

    name = "search_mealie_mealplan"

    description = (
        "Search the household Mealie recipe database for the meal plan for particular days. "
        "Use this tool when the user asks about the meal plan for a particular day, including asking about dinner, lunch, breakfast, or other meals for the day. "
        "Returns a list of recipes for the specified days. "
        "If the user refers to the current day, always call assist__GetDateTime before searching for the meal plan. Do not rely on system time to determine the current day. "
    )

    parameters = vol.Schema(
        {
            vol.Required(
                "start date",
                description="Start date for the meal plan. Formatted as YYYY-MM-DD.",
            ): str,
            vol.Required(
                "end date",
                description="End date for the meal plan. Formatted as YYYY-MM-DD.",
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
        start_date = data["start date"]
        end_date = data["end date"]

        entries = hass.config_entries.async_entries("mealie")

        if not entries:
            return {
                "error": "No Mealie integration configured"
            }

        mealie_entry = entries[0]

        response = await hass.services.async_call(
            "mealie",
            "get_mealplan",
            {
                "config_entry_id": mealie_entry.entry_id,
                "start_date": start_date,
                "end_date": end_date
            },
            blocking=True,
            return_response=True,
        )

        if response is None:
            return {"error": "Mealie returned no response"}

        return cast(JsonObjectType, response)

class MealieAddToMealplanTool(llm.Tool):
    """Tool for adding recipes to Mealie meal plans."""

    name = "add_to_mealie_mealplan"

    description = (
        "Add a recipe the household Mealie meal plan for particular days. "
        "Returns the list of recipes in the meal plan for the day that the new recipe is added to. "
        "Use this returned value to confirm that the recipe was added successfully. "
        "If the user refers to the current day, always call assist__GetDateTime before adding to the meal plan. Do not rely on system time to determine the current day. "
        # "Never call this tool unless you have already searched recipes and have the recipe_id. "
        # "If the user asks for a recipe to be added to the meal plan and you have not already presented a meal option, search for a recipe first and then confirm with the user before adding to the meal plan."
    )

    parameters = vol.Schema(
        {
            vol.Required(
                "date",
                description="Date for the meal plan. Formatted as YYYY-MM-DD.",
            ): str,
            vol.Required(
                "entry_type",
                description="Type of meal to add to the meal plan. The only valid values are 'breakfast', 'lunch', 'dinner', 'side', 'dessert', 'snack', and 'drink'. Choose one of these types according chat history, otherwise choose according to the kind of meal the user wants to add.",
            ): str,
            vol.Required(
                "recipe_id",
                description="recipe_id of the recipe to add to the meal plan.",
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
        date = data["date"]
        entry_type = data["entry_type"]
        recipe_id = data["recipe_id"]

        entries = hass.config_entries.async_entries("mealie")

        if not entries:
            return {
                "error": "No Mealie integration configured"
            }

        mealie_entry = entries[0]

        response = await hass.services.async_call(
            "mealie",
            "set_mealplan",
            {
                "config_entry_id": mealie_entry.entry_id,
                "date": date,
                "entry_type": entry_type,
                "recipe_id": recipe_id
            },
            blocking=True,
            return_response=True,
        )

        if response is None:
            return {"error": "Mealie returned no response when adding to meal plan."}

        response = await hass.services.async_call(
            "mealie",
            "get_mealplan",
            {
                "config_entry_id": mealie_entry.entry_id,
                "start_date": date,
                "end_date": date
            },
            blocking=True,
            return_response=True,
        )

        if response is None:
            return {"error": "Mealie returned no response when requesting new meal plan."}

        return cast(JsonObjectType, response)

class MealieLLMAPI(llm.API):
    """Expose Mealie tools to Assist."""

    id = DOMAIN

    async def async_get_api_instance(
        self,
        llm_context: llm.LLMContext
    ) -> llm.APIInstance:
        return llm.APIInstance(
            self, 
            "Always use these tools to search the household Mealie recipe database when the user asks to find or look up recipes.", 
            llm_context, 
            [
                MealieRecipeSearchTool(), 
                MealieRecipeDetailsTool(), 
                MealieMealplanSearchTool(),
                MealieAddToMealplanTool(),
            ]
        )

async def async_setup_llm(hass: HomeAssistant):
    """Register the Mealie LLM API with Home Assistant."""
    if any(api.id == DOMAIN for api in llm.async_get_apis(hass)):
        return

    api = MealieLLMAPI(hass=hass, id=DOMAIN, name="Mealie Recipes")

    llm.async_register_api(
        hass,
        api,
    )