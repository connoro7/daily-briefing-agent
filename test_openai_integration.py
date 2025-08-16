#!/usr/bin/env python3
"""Test script to verify OpenAI integration with the daily briefing agent."""

import os
from daily_briefing_abt import DailyBriefingAgent

def test_openai_integration():
    """Test the OpenAI integration in the daily briefing agent"""
    
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please set the OPENAI_API_KEY environment variable")
        return False
    
    print("✅ OPENAI_API_KEY found in environment")
    print(f"🔑 API Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else api_key}")
    
    try:
        print("\n🤖 Creating DailyBriefingAgent with OpenAI integration...")
        agent = DailyBriefingAgent()
        print("✅ Agent created successfully")
        
        print("\n🌍 Testing briefing generation with OpenAI...")
        briefing = agent.generate_briefing(location="New York", topic="technology")
        
        if briefing and not briefing.startswith("❌"):
            print("✅ OpenAI integration working successfully!")
            print("\n" + "="*60)
            print("🚀 OPENAI-POWERED DAILY BRIEFING:")
            print("="*60)
            print(briefing)
            print("="*60)
            return True
        else:
            print("❌ Failed to generate briefing")
            print(briefing)
            return False
            
    except Exception as e:
        print(f"❌ Error testing OpenAI integration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_openai_integration()
    if success:
        print("\n🎉 OpenAI integration test PASSED!")
    else:
        print("\n💥 OpenAI integration test FAILED!")