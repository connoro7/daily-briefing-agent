# Daily Briefing Agent with Sub-Agent Spawning Architecture

This is a re-implementation of the daily briefing agent using **Agentic Behavior Trees (ABT)** pattern inspired by Chapter 6 of "AI Agents in Action".

## Architecture Overview

The implementation uses a **sub-agent spawning structure** where specialized agents handle different aspects of the briefing generation:

### Sub-Agents
1. **WeatherAgent**: Specialized in weather data collection
2. **NewsAgent**: Specialized in news headline gathering  
3. **SynthesizerAgent**: Combines data and generates human-readable briefings

### Behavior Tree Structure
```
DailyBriefingSequence (Root)
├── DataGathering (Parallel)
│   ├── WeatherCollection (Action)
│   └── NewsCollection (Action)
├── DataReadyCheck (Condition)
└── BriefingSynthesis (Action)
```

## Key Features

✅ **Sub-Agent Spawning**: Each agent is specialized and autonomous
✅ **Behavior Tree Control**: Uses py_trees for orchestration
✅ **Parallel Execution**: Weather and news gathering happen simultaneously
✅ **State Management**: Agents maintain independent state
✅ **Error Handling**: Robust failure handling at each node
✅ **Modular Design**: Easy to add new sub-agents and capabilities

## Requirements Met

All requirements from the specification are implemented:

- ✅ Weather checker tool with location parameter
- ✅ News fetcher tool with topic and count parameters
- ✅ Multi-stage workflow (trigger → gather → synthesize → output)
- ✅ Human-readable output format
- ✅ Extensible architecture for additional tools

## Installation and Usage

```bash
# Install dependencies
pip install -r requirements_briefing.txt

# Run the agent
python daily_briefing_abt.py
```

## Example Output

```
🌅 Daily Briefing - December 15, 2024

📍 Weather Update for San Francisco:
Temperature: 18°C
Conditions: Foggy

📰 Top Technology News Headlines:
1. AI Breakthrough: New Language Model Achieves Human-Level Performance
2. Tech Giants Report Strong Q3 Earnings Despite Market Volatility
3. Quantum Computing Milestone Reached by Leading Research Team

📊 Briefing Summary:
Today's weather in San Francisco shows foggy conditions with a temperature of 18°C. 
In technology news, we're seeing 3 significant developments that may impact your day.

Stay informed and have a great day! 🌟
```

## Technical Implementation

### Behavior Tree Pattern
- Uses **Sequence** nodes for ordered execution
- Uses **Parallel** nodes for concurrent data gathering
- Uses **Condition** nodes for data validation
- Implements **SubAgentAction** nodes for agent execution

### State Management
- **Blackboard pattern** for shared state between nodes
- Each sub-agent maintains independent state
- Context passing through blackboard system

### Extensibility
- Easy to add new sub-agents by extending `SubAgent` base class
- New behavior tree nodes can be added for complex workflows
- Plugin-style architecture for additional data sources

## Future Enhancements

- Integration with real weather and news APIs
- LLM integration for more sophisticated synthesis
- Error recovery and retry mechanisms
- Configuration-driven agent spawning
- Metrics and monitoring capabilities