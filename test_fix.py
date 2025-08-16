#!/usr/bin/env python3
"""Test script to verify the blackboard fix works."""

try:
    from daily_briefing_abt import DailyBriefingAgent
    
    print("✅ Successfully imported DailyBriefingAgent")
    
    # Create and test the agent
    agent = DailyBriefingAgent()
    print("✅ Successfully created DailyBriefingAgent instance")
    
    # Test with simple parameters
    briefing = agent.generate_briefing(location="San Francisco", topic="technology")
    
    if briefing and not briefing.startswith("❌"):
        print("✅ Successfully generated briefing!")
        print("\n" + "="*50)
        print("SAMPLE BRIEFING:")
        print("="*50)
        print(briefing)
    else:
        print("❌ Failed to generate briefing")
        print(briefing)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()