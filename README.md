# Mealie LLM Assistant Tools

A Home Assistant custom component that integrates your [Mealie](https://mealie.io/) recipe database with Home Assistant's LLM (Large Language Model) tools. This allows your voice assistants and AI assistants to search and retrieve recipes from your personal recipe collection.

This builds on top of the Home Assistant built-in Mealie integration because, unfortunately, the built-in plugin does not provide any LLM Tools.

## Features

- **LLM Integration / Voice Assistant Support** - Works seamlessly with Home Assistant's LLM platform (compatible with any LLM provider). Ask your voice assistant to find recipes from your Mealie database
- **Recipe Searching** - Find recipes by name or search phrase with a quick overview or get full recipe information including ingredients and instructions
- **Meal Planning** - Read your mealie meal plan or ask to add a recipe to your meal plan.

## Requirements

- Home Assistant 2026.2.3 or later
- [Mealie](https://mealie.io/) self-hosted recipe manager
- [Home Assistant Mealie Integration](https://www.home-assistant.io/integrations/mealie/) configured and working

## Installation

### HACS (Recommended)

1. Open **HACS** in Home Assistant
2. Go to **Integrations**
3. Click the **⋯** (menu) button and select **Custom repositories**
4. Add this repository: `https://github.com/CalebBerhow/ha_mealie_llm`
5. Search for **Mealie LLM Assistant Tools**
6. Click **Install**
7. Restart Home Assistant

### Manual Installation

1. Clone this repository to your Home Assistant `custom_components` directory:
   ```bash
   git clone https://github.com/CalebBerhow/ha_mealie_llm.git
   mv ha_mealie_llm/custom_components/mealie_llm ~/.homeassistant/custom_components/
   ```
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services** → **Integrations**
2. Click **Create Integration** and search for **Mealie LLM Assistant Tools**
3. Follow the setup wizard
4. Ensure you already have the [Mealie integration](https://github.com/BallAerospace/home-assistant-mealie) installed and configured

## Usage

### With Voice Assistants

Once configured, your voice assistants (like Assist) can use these tools automatically:

**Example voice commands:**
- "Find me a pasta recipe"
- "Search for chicken recipes"
- "What's in the chicken parmesan recipe?"
- "Show me the details for chocolate cake"

## Troubleshooting

### No recipes returned
- Ensure the Mealie integration is properly configured and connected
- Verify your Mealie instance is accessible from Home Assistant
- Check that recipes exist in your Mealie database

### "No Mealie integration configured" error
- Install and configure the [Home Assistant Mealie integration](https://github.com/BallAerospace/home-assistant-mealie)
- Restart Home Assistant after configuring Mealie

### Voice assistant not finding the tools
- Restart Home Assistant after installing this integration
- Verify that an LLM provider is configured in your Home Assistant and has the "Mealie Recipes" API enabled.

## Development

### Prerequisites

You'll need Python 3.14.2, a virtual environment, and the project dependencies installed.

#### Windows

1. **Install Python 3.14.2**
   ```powershell
   # Download and install Python 3.14.2 from https://www.python.org/downloads/
   # Or use Windows Package Manager (winget)
   winget install Python.Python.3.14
   
   # Verify installation
   python --version
   ```

2. **Create virtual environment**
   ```powershell
   # Navigate to the project directory
   cd ha_mealie_llm
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   # Upgrade pip
   python -m pip install --upgrade pip
   
   # Install requirements
   pip install -r requirements.txt
   ```

#### Linux (Ubuntu/Debian)

1. **Install Python 3.14.2**
   ```bash
   # Update package manager
   sudo apt-get update
   
   # Install Python 3.14.2
   sudo apt-get install python3.14
   
   # Verify installation
   python3 --version
   ```

2. **Create virtual environment**
   ```bash
   # Navigate to the project directory
   cd ha_mealie_llm
   
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Upgrade pip
   python -m pip install --upgrade pip
   
   # Install requirements
   pip install -r requirements.txt
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- Built for [Home Assistant](https://www.home-assistant.io/)
- Integrates with [Mealie](https://mealie.io/)
- Author: [@CalebBerhow](https://github.com/CalebBerhow)
