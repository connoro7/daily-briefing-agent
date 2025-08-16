# Daily Briefing Agent Using Sub-Agent Pattern

## Installation
This project is managed with `uv`.

To install:
1. Ensure that `OPENAI_API_KEY` is present in your environment
2. `git clone` this project
3. `cd /path/to/daily-briefing-agent`
4. `uv sync`
5. `source .venv/bin/activate`

To run:
`uv run daily_briefing_abt.py`

The tests will run first, and then the application will enter into interactive mode.
From there, enter your location and the news category you would like to read from.

Example output:
```
🔍 Agent States:
  weather_agent: 1 items in state
  news_agent: 1 items in state
  synthesizer_agent: 1 items in state

==================================================

🎯 Interactive Mode
Enter 'quit' to exit

------------------------------
Enter location (default: San Francisco): Finland
Enter news topic (default: technology): secret underground lizard civilizations

🎯 Generating briefing for Finland, secret underground lizard civilizations...
🤖 Daily Briefing Agent Starting...
==================================================
🌳 Executing Agentic Behavior Tree...
[WeatherAgent] Gathering weather data for Finland...
[WeatherAgent] Weather data collected: {'location': 'Finland', 'temperature': -2, 'condition': 'Partly Cloudy', 'humidity': 78, 'timestamp': '2025-08-16T13:31:32.726329'}
[NewsAgent] Gathering news headlines for topic: secret underground lizard civilizations...
[NewsAgent] News data collected: 3 headlines
[SynthesizerAgent] Synthesizing daily briefing...
[SynthesizerAgent] Daily briefing generated successfully

✅ Daily Briefing Generated Successfully!
==================================================
🗓️  **Daily Briefing - August 16, 2025**

🌦️  **Weather Update:** In Finland, the temperature currently stands at -2°C with partly cloudy conditions. The humidity level is at 78%. Despite the chilly weather, it's a great day to enjoy the unique beauty of Finland with its picturesque landscapes.

📰 **News Headlines - Secret Underground Lizard Civilizations:**
1. **Scientists Uncover Evidence in Antarctica:** Researchers have made a groundbreaking discovery, revealing evidence of a secret underground lizard civilization in Antarctica. This finding opens up new possibilities for understanding the mysteries of the continent's past.

2. **Ancient Lizard Society Beneath Egypt's Pyramids:** A recent study suggests the existence of an ancient underground lizard society beneath Egypt's pyramids. This revelation could reshape our understanding of history and the interconnectedness of civilizations.

3. **Whistleblower Exposes Hidden Lizard Kingdom:** A government whistleblower has come forward to reveal the existence of a hidden lizard kingdom beneath a major city. The disclosure has sparked intrigue and raised questions about what lies beneath our urban landscapes.

🔍 **Brief Summary:** Today's briefing uncovered fascinating revelations about secret underground lizard civilizations, spanning from Antarctica to Egypt and major cities. These discoveries challenge conventional wisdom and ignite curiosity about the hidden realms beneath our feet.

Stay informed, stay curious! 🦎 #DailyBriefing #LizardCivilizations

------------------------------
```
