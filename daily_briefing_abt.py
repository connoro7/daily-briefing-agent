#!/usr/bin/env python3
"""
Daily Briefing Agent with Sub-Agent Spawning Architecture
Re-implementation using Agentic Behavior Trees (ABT) pattern

This implementation follows the behavior tree concepts from Chapter 6 and
meets all requirements from the briefing agent specification.
"""

import py_trees
import os
from typing import Any
from datetime import datetime
from abc import ABC, abstractmethod
from openai import OpenAI


# ============================================================================
# OpenAI Configuration
# ============================================================================

# Initialize OpenAI client (API key from environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        Get current weather data using OpenAI to simulate weather API
        In production, this would be replaced with actual weather API calls
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a weather API that provides current weather data. Return realistic current weather information in JSON format with temperature (Celsius), condition, and any other relevant details. Be concise and realistic for the specified location and current season.",
                    },
                    {
                        "role": "user",
                        "content": f"Get current weather for {location}. Return only a JSON object with 'temperature' (number in Celsius), 'condition' (string), and 'humidity' (percentage).",
                    },
                ],
                temperature=0.7,
                max_tokens=150,
            )

            # Parse the JSON response
            weather_text = response.choices[0].message.content.strip()

            # Try to extract JSON from the response
            try:
                import json

                # Find JSON in the response (it might have extra text)
                start = weather_text.find("{")
                end = weather_text.rfind("}") + 1
                if start != -1 and end != 0:
                    weather_json = json.loads(weather_text[start:end])

                    return {
                        "location": location,
                        "temperature": weather_json.get("temperature", 20),
                        "condition": weather_json.get("condition", "Clear"),
                        "humidity": weather_json.get("humidity", 50),
                        "timestamp": datetime.now().isoformat(),
                    }
            except (json.JSONDecodeError, KeyError):
                # Fallback to parsing the text response
                pass

        except Exception as e:
            print(f"[{self.name}] OpenAI API error: {e}, using fallback data")

        # Fallback weather data if OpenAI fails
        fallback_data = {
            "New York": {
                "temperature": 22,
                "condition": "Partly Cloudy",
                "humidity": 65,
            },
            "London": {"temperature": 15, "condition": "Rainy", "humidity": 80},
            "Tokyo": {"temperature": 25, "condition": "Sunny", "humidity": 45},
            "San Francisco": {"temperature": 18, "condition": "Foggy", "humidity": 75},
            "Default": {"temperature": 20, "condition": "Clear", "humidity": 50},
        }

        weather = fallback_data.get(location, fallback_data["Default"])
        return {
            "location": location,
            "temperature": weather["temperature"],
            "condition": weather["condition"],
            "humidity": weather["humidity"],
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
        Get current news headlines using OpenAI to simulate news API
        In production, this would be replaced with actual news API calls
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a news API that provides current headlines. Generate {count} realistic, current news headlines for the topic '{topic}'. Headlines should be believable and reflect current events/trends. Return only a JSON array of headline strings, no other text.",
                    },
                    {
                        "role": "user",
                        "content": f'Generate {count} current {topic} news headlines. Return as JSON array: ["headline1", "headline2", ...]',
                    },
                ],
                temperature=0.8,
                max_tokens=200,
            )

            # Parse the JSON response
            headlines_text = response.choices[0].message.content.strip()

            try:
                import json

                # Find JSON array in the response
                start = headlines_text.find("[")
                end = headlines_text.rfind("]") + 1
                if start != -1 and end != 0:
                    headlines_json = json.loads(headlines_text[start:end])

                    # Ensure we have the right number of headlines
                    headlines = (
                        headlines_json[:count]
                        if isinstance(headlines_json, list)
                        else []
                    )

                    return {
                        "topic": topic,
                        "headlines": headlines,
                        "count": len(headlines),
                        "timestamp": datetime.now().isoformat(),
                    }
            except (json.JSONDecodeError, KeyError):
                # Fallback to parsing text manually
                pass

        except Exception as e:
            print(f"[{self.name}] OpenAI API error: {e}, using fallback data")

        # Fallback news headlines if OpenAI fails
        fallback_headlines = {
            "technology": [
                "AI Breakthrough: New Language Model Achieves Human-Level Performance",
                "Tech Giants Report Strong Q3 Earnings Despite Market Volatility",
                "Quantum Computing Milestone Reached by Leading Research Team",
                "Cybersecurity Concerns Rise as Attacks Become More Sophisticated",
                "New Smartphone Technology Promises Longer Battery Life",
            ],
            "world": [
                "Global Climate Summit Announces New Sustainability Initiatives",
                "International Trade Agreements Show Positive Economic Impact",
                "Space Agency Successfully Launches New Mars Exploration Mission",
                "Diplomatic Relations Strengthen Between Allied Nations",
                "Education Reform Shows Promising Results in Recent Studies",
            ],
            "business": [
                "Stock Markets Reach New Heights Amid Economic Recovery",
                "Renewable Energy Sector Sees Record Investment Growth",
                "Cryptocurrency Market Shows Signs of Stabilization",
                "Small Business Lending Programs See Increased Participation",
                "Remote Work Trends Continue to Shape Corporate Policies",
            ],
        }

        headlines = fallback_headlines.get(topic.lower(), fallback_headlines["world"])[
            :count
        ]

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
        Synthesize collected data into a human-readable daily briefing using OpenAI
        """
        location = weather_data.get("location", "Unknown")
        temperature = weather_data.get("temperature", "N/A")
        condition = weather_data.get("condition", "N/A")
        humidity = weather_data.get("humidity", "N/A")

        topic = news_data.get("topic", "general")
        headlines = news_data.get("headlines", [])

        try:
            # Prepare data for OpenAI
            weather_summary = f"Location: {location}, Temperature: {temperature}°C, Conditions: {condition}"
            if humidity != "N/A":
                weather_summary += f", Humidity: {humidity}%"

            headlines_text = "\n".join([f"- {headline}" for headline in headlines])

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional news briefing assistant. Create a well-formatted, engaging daily briefing that combines weather and news information. Use emojis appropriately, maintain a professional yet friendly tone, and provide useful insights. Structure the briefing with clear sections.",
                    },
                    {
                        "role": "user",
                        "content": f"""Create a daily briefing for {datetime.now().strftime("%B %d, %Y")} with this information:

WEATHER DATA:
{weather_summary}

NEWS HEADLINES ({topic.title()}):
{headlines_text}

Please create an engaging, well-formatted daily briefing that includes:
1. A header with the date
2. Weather section with relevant insights
3. News section with the headlines
4. A brief summary/conclusion
5. Use appropriate emojis and formatting

Keep it professional but engaging, around 200-300 words.""",
                    },
                ],
                temperature=0.7,
                max_tokens=500,
            )

            briefing = response.choices[0].message.content.strip()
            return briefing

        except Exception as e:
            print(f"[{self.name}] OpenAI API error: {e}, using fallback template")

            # Fallback to template-based briefing if OpenAI fails
            briefing = f"""🌅 Daily Briefing - {datetime.now().strftime("%B %d, %Y")}

📍 Weather Update for {location}:
Temperature: {temperature}°C
Conditions: {condition}
{f"Humidity: {humidity}%" if humidity != "N/A" else ""}

📰 Top {topic.title()} News Headlines:
"""

            for i, headline in enumerate(headlines, 1):
                briefing += f"{i}. {headline}\n"

            briefing += f"""
📊 Briefing Summary:
Today's weather in {location} shows {condition.lower() if condition != "N/A" else "current"} conditions with a temperature of {temperature}°C.
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

    def __init__(
        self,
        name: str,
        sub_agent: SubAgent,
        context_key: str = None,
        shared_state: dict = None,
    ):
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
            "briefing": None,
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
            shared_state=self.shared_state,
        )

        news_action = SubAgentAction(
            name="NewsCollection",
            sub_agent=self.news_agent,
            context_key="news_data",
            shared_state=self.shared_state,
        )

        data_gathering.add_children([weather_action, news_action])

        # Data readiness condition
        data_ready_condition = BriefingCondition(
            name="DataReadyCheck", shared_state=self.shared_state
        )

        # Synthesis phase
        synthesis_action = SubAgentAction(
            name="BriefingSynthesis",
            sub_agent=self.synthesizer_agent,
            context_key="briefing",
            shared_state=self.shared_state,
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
        self.shared_state["context"] = {
            "location": location,
            "topic": topic,
            "news_count": 3,
        }

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
