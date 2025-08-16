#!/usr/bin/env python3
"""
Daily Briefing Agent with Sub-Agent Spawning Architecture
Re-implementation using Agentic Behavior Trees (ABT) pattern

This implementation follows the behavior tree concepts from Chapter 6 and
meets all requirements from the briefing agent specification.
"""

import py_trees
import json
import requests
import time
import textwrap
from typing import Any
from datetime import datetime
from abc import ABC, abstractmethod


# ============================================================================
# Sub-Agent Base Classes and Implementations
# ============================================================================


class SubAgent(ABC):
    """Base class for all sub-agents in the system"""

    def __init__(self, name: str):
        self.name = name
        self.state = {}

    @abstractmethod
    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute the sub-agent's specialized task"""
        pass


class WeatherAgent(SubAgent):
    """Specialized sub-agent for weather data collection"""

    def __init__(self):
        super().__init__("WeatherAgent")

    def get_weather(self, location: str) -> dict:
        """
        Mock weather API call - in production, integrate with real weather service
        Returns weather data for the specified location
        """
        # Mock weather data - replace with actual API call
        mock_weather_data = {
            "New York": {"temperature": 72, "condition": "Partly Cloudy"},
            "London": {"temperature": 15, "condition": "Rainy"},
            "Tokyo": {"temperature": 25, "condition": "Sunny"},
            "San Francisco": {"temperature": 18, "condition": "Foggy"},
            "Default": {"temperature": 20, "condition": "Clear"},
        }

        weather = mock_weather_data.get(location, mock_weather_data["Default"])

        return {
            "location": location,
            "temperature": weather["temperature"],
            "condition": weather["condition"],
            "timestamp": datetime.now().isoformat(),
        }

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute weather data collection"""
        location = context.get("location", "San Francisco")

        print(f"[{self.name}] Gathering weather data for {location}...")
        weather_data = self.get_weather(location)

        self.state["weather_data"] = weather_data
        print(f"[{self.name}] Weather data collected: {weather_data}")

        return {"status": "success", "data": weather_data, "agent": self.name}


class NewsAgent(SubAgent):
    """Specialized sub-agent for news headline collection"""

    def __init__(self):
        super().__init__("NewsAgent")

    def get_top_headlines(self, topic: str, count: int = 3) -> dict:
        """
        Mock news API call - in production, integrate with real news service
        Returns top headlines for the specified topic
        """
        # Mock news headlines - replace with actual API call
        mock_headlines = {
            "technology": [
                "AI Breakthrough: New Language Model Achieves Human-Level Performance",
                "Tech Giants Report Strong Q3 Earnings Despite Market Volatility",
                "Quantum Computing Milestone Reached by Leading Research Team",
            ],
            "world": [
                "Global Climate Summit Announces New Sustainability Initiatives",
                "International Trade Agreements Show Positive Economic Impact",
                "Space Agency Successfully Launches New Mars Exploration Mission",
            ],
            "business": [
                "Stock Markets Reach New Heights Amid Economic Recovery",
                "Renewable Energy Sector Sees Record Investment Growth",
                "Cryptocurrency Market Shows Signs of Stabilization",
            ],
        }

        headlines = mock_headlines.get(topic.lower(), mock_headlines["world"])[:count]

        return {
            "topic": topic,
            "headlines": headlines,
            "count": len(headlines),
            "timestamp": datetime.now().isoformat(),
        }

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute news data collection"""
        topic = context.get("topic", "technology")
        count = context.get("news_count", 3)

        print(f"[{self.name}] Gathering news headlines for topic: {topic}...")
        news_data = self.get_top_headlines(topic, count)

        self.state["news_data"] = news_data
        print(
            f"[{self.name}] News data collected: {len(news_data['headlines'])} headlines"
        )

        return {"status": "success", "data": news_data, "agent": self.name}


class SynthesizerAgent(SubAgent):
    """Specialized sub-agent for data synthesis and briefing generation"""

    def __init__(self):
        super().__init__("SynthesizerAgent")

    def synthesize_briefing(
        self, weather_data: dict, news_data: dict, context: dict
    ) -> str:
        """
        Synthesize collected data into a human-readable daily briefing
        In production, this would use an LLM API call
        """
        location = weather_data.get("location", "Unknown")
        temperature = weather_data.get("temperature", "N/A")
        condition = weather_data.get("condition", "N/A")

        topic = news_data.get("topic", "general")
        headlines = news_data.get("headlines", [])

        # Generate briefing using template (replace with LLM call in production)
        briefing = f"""
🌅 Daily Briefing - {datetime.now().strftime("%B %d, %Y")}

📍 Weather Update for {location}:
Temperature: {temperature}°C
Conditions: {condition}

📰 Top {topic.title()} News Headlines:
"""

        for i, headline in enumerate(headlines, 1):
            briefing += f"{i}. {headline}\n"

        briefing += f"""
📊 Briefing Summary:
Today's weather in {location} shows {condition.lower()} conditions with a temperature of {temperature}°C.
In {topic} news, we're seeing {len(headlines)} significant developments that may impact your day.

Stay informed and have a great day! 🌟
"""

        return briefing.strip()

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute data synthesis and briefing generation"""
        weather_data = context.get("weather_data", {})
        news_data = context.get("news_data", {})

        print(f"[{self.name}] Synthesizing daily briefing...")
        briefing = self.synthesize_briefing(weather_data, news_data, context)

        self.state["briefing"] = briefing
        print(f"[{self.name}] Daily briefing generated successfully")

        return {"status": "success", "data": {"briefing": briefing}, "agent": self.name}


# ============================================================================
# Behavior Tree Node Implementations
# ============================================================================


class SubAgentAction(py_trees.behaviour.Behaviour):
    """Behavior tree action node that executes a sub-agent"""

    def __init__(self, name: str, sub_agent: SubAgent, context_key: str = None, shared_state: dict = None):
        super().__init__(name)
        self.sub_agent = sub_agent
        self.context_key = context_key
        self.shared_state = shared_state

    def update(self):
        """Execute the sub-agent and update behavior tree state"""
        try:
            # Get context from shared state
            context = self.shared_state.get("context", {}).copy()
            
            # For the SynthesizerAgent, add collected data to context
            if self.sub_agent.name == "SynthesizerAgent":
                context["weather_data"] = self.shared_state.get("weather_data", {})
                context["news_data"] = self.shared_state.get("news_data", {})

            # Execute sub-agent
            result = self.sub_agent.execute(context)

            # Store result in shared state
            if self.context_key and result.get("status") == "success":
                self.shared_state[self.context_key] = result["data"]

            return py_trees.common.Status.SUCCESS

        except Exception as e:
            self.logger.error(f"Sub-agent {self.sub_agent.name} failed: {str(e)}")
            return py_trees.common.Status.FAILURE


class BriefingCondition(py_trees.behaviour.Behaviour):
    """Condition node that checks if briefing data is ready"""

    def __init__(self, name: str, shared_state: dict = None):
        super().__init__(name)
        self.shared_state = shared_state

    def update(self):
        """Check if all required data is available for briefing generation"""
        weather_data = self.shared_state.get("weather_data")
        news_data = self.shared_state.get("news_data")

        if weather_data and news_data:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


# ============================================================================
# Main Daily Briefing Agent with ABT Architecture
# ============================================================================


class DailyBriefingAgent:
    """
    Main agent that orchestrates sub-agents using Agentic Behavior Tree pattern
    """

    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.news_agent = NewsAgent()
        self.synthesizer_agent = SynthesizerAgent()
        self.behavior_tree = None
        self._setup_behavior_tree()

    def _setup_behavior_tree(self):
        """Setup the agentic behavior tree structure"""

        # Initialize shared state instead of blackboard for simplicity
        self.shared_state = {
            "context": {},
            "weather_data": None,
            "news_data": None,
            "briefing": None
        }

        # Create behavior tree structure
        root = py_trees.composites.Sequence(name="DailyBriefingSequence", memory=True)

        # Parallel data gathering phase
        data_gathering = py_trees.composites.Parallel(
            name="DataGathering", policy=py_trees.common.ParallelPolicy.SuccessOnAll()
        )

        # Add sub-agent actions
        weather_action = SubAgentAction(
            name="WeatherCollection",
            sub_agent=self.weather_agent,
            context_key="weather_data",
            shared_state=self.shared_state
        )

        news_action = SubAgentAction(
            name="NewsCollection", 
            sub_agent=self.news_agent, 
            context_key="news_data",
            shared_state=self.shared_state
        )

        data_gathering.add_children([weather_action, news_action])

        # Data readiness condition
        data_ready_condition = BriefingCondition(name="DataReadyCheck", shared_state=self.shared_state)

        # Synthesis phase
        synthesis_action = SubAgentAction(
            name="BriefingSynthesis",
            sub_agent=self.synthesizer_agent,
            context_key="briefing",
            shared_state=self.shared_state
        )

        # Assemble the tree
        root.add_children([data_gathering, data_ready_condition, synthesis_action])

        self.behavior_tree = py_trees.trees.BehaviourTree(root)

    def generate_briefing(
        self, location: str = "San Francisco", topic: str = "technology"
    ) -> str:
        """
        Generate a daily briefing using the sub-agent spawning architecture

        Args:
            location: Location for weather data
            topic: Topic for news headlines

        Returns:
            Generated daily briefing text
        """
        print("🤖 Daily Briefing Agent Starting...")
        print("=" * 50)

        # Set context in shared state
        self.shared_state["context"] = {"location": location, "topic": topic, "news_count": 3}

        # Execute behavior tree
        print("🌳 Executing Agentic Behavior Tree...")
        self.behavior_tree.tick()

        # Get final briefing
        briefing_data = self.shared_state.get("briefing")
        if briefing_data and "briefing" in briefing_data:
            briefing = briefing_data["briefing"]
            print("\n✅ Daily Briefing Generated Successfully!")
            print("=" * 50)
            return briefing
        else:
            error_msg = "❌ Failed to generate daily briefing"
            print(error_msg)
            return error_msg

    def get_agent_states(self) -> dict[str, Any]:
        """Get the current state of all sub-agents"""
        return {
            "weather_agent": self.weather_agent.state,
            "news_agent": self.news_agent.state,
            "synthesizer_agent": self.synthesizer_agent.state,
        }


# ============================================================================
# Demo and Testing Functions
# ============================================================================


def demo_briefing_agent():
    """Demonstrate the daily briefing agent functionality"""
    print("🚀 Daily Briefing Agent Demo")
    print("=" * 50)

    # Create agent instance
    agent = DailyBriefingAgent()

    # Test cases
    test_cases = [
        {"location": "New York", "topic": "technology"},
        {"location": "London", "topic": "world"},
        {"location": "Tokyo", "topic": "business"},
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case}")
        print("-" * 30)

        briefing = agent.generate_briefing(**test_case)
        print(briefing)

        # Show agent states
        print(f"\n🔍 Agent States:")
        states = agent.get_agent_states()
        for agent_name, state in states.items():
            print(f"  {agent_name}: {len(state)} items in state")

        print("\n" + "=" * 50)


def main():
    """Main entry point for the daily briefing agent"""
    try:
        # Set up py_trees logging
        py_trees.logging.level = py_trees.logging.Level.INFO

        # Run demo
        demo_briefing_agent()

        # Interactive mode
        print("\n🎯 Interactive Mode")
        print("Enter 'quit' to exit")

        agent = DailyBriefingAgent()

        while True:
            print("\n" + "-" * 30)
            location = input("Enter location (default: San Francisco): ").strip()
            if location.lower() == "quit":
                break
            if not location:
                location = "San Francisco"

            topic = input("Enter news topic (default: technology): ").strip()
            if topic.lower() == "quit":
                break
            if not topic:
                topic = "technology"

            print(f"\n🎯 Generating briefing for {location}, {topic}...")
            briefing = agent.generate_briefing(location=location, topic=topic)
            print(briefing)

        print("\n👋 Thank you for using Daily Briefing Agent!")

    except KeyboardInterrupt:
        print("\n\n👋 Daily Briefing Agent interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
