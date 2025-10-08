#!/usr/bin/env python3
"""
Test script for AG UI integration
Tests the FastAPI backend endpoints and data flow
"""

import requests
import json
from datetime import datetime

# Test configuration
BACKEND_URL = "http://localhost:8001"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_tools_endpoint():
    """Test the tools listing endpoint"""
    print("\n🔍 Testing tools endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/tools")
        if response.status_code == 200:
            data = response.json()
            tools = data.get('tools', [])
            print(f"✅ Tools endpoint passed: Found {len(tools)} tools")
            for tool in tools[:3]:  # Show first 3 tools
                print(f"   - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')[:50]}...")
            return True
        else:
            print(f"❌ Tools endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Tools endpoint error: {e}")
        return False

def test_visualization_endpoint():
    """Test the visualization data endpoint"""
    print("\n🔍 Testing visualization endpoint...")
    try:
        test_data = {
            "data_type": "statistics",
            "session_id": "session_001"
        }
        response = requests.post(f"{BACKEND_URL}/visualize", json=test_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Visualization endpoint passed: {data['data_type']}")
            print(f"   Data keys: {list(data['data'].keys()) if isinstance(data['data'], dict) else 'Non-dict data'}")
            return True
        else:
            print(f"❌ Visualization endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Visualization endpoint error: {e}")
        return False

def test_circumplex_endpoint():
    """Test the circumplex data endpoint"""
    print("\n🔍 Testing circumplex endpoint...")
    try:
        test_data = {
            "data_type": "emotions",
            "query": "emotional patterns",
            "session_id": "session_001"
        }
        response = requests.post(f"{BACKEND_URL}/circumplex", json=test_data)
        if response.status_code == 200:
            data = response.json()
            emotions = data.get('emotions', [])
            print(f"✅ Circumplex endpoint passed: Found {len(emotions)} emotions")
            if emotions:
                print(f"   Sample emotion: {emotions[0]}")
            return True
        else:
            print(f"❌ Circumplex endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Circumplex endpoint error: {e}")
        return False

def test_deep_agent_endpoint():
    """Test the deep agent state endpoint"""
    print("\n🔍 Testing deep agent endpoint...")
    try:
        response = requests.post(f"{BACKEND_URL}/deep_agent")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Deep agent endpoint passed: Status = {data.get('status', 'unknown')}")
            print(f"   Current task: {data.get('current_task', 'None')}")
            print(f"   TODOs: {len(data.get('todos', []))}")
            print(f"   Thoughts: {len(data.get('thoughts', []))}")
            return True
        else:
            print(f"❌ Deep agent endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Deep agent endpoint error: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint with a simple message"""
    print("\n🔍 Testing chat endpoint...")
    try:
        test_data = {
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, can you help me analyze psychological data?",
                    "id": "test_msg_1"
                }
            ],
            "thread_id": "test_thread"
        }
        response = requests.post(f"{BACKEND_URL}/chat", json=test_data)
        if response.status_code == 200:
            data = response.json()
            message = data.get('message', {})
            print(f"✅ Chat endpoint passed")
            print(f"   Response: {message.get('content', 'No content')[:100]}...")
            return True
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting AG UI Integration Tests")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_tools_endpoint,
        test_visualization_endpoint,
        test_circumplex_endpoint,
        test_deep_agent_endpoint,
        test_chat_endpoint,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AG UI integration is working correctly.")
        print("\n📋 Next steps:")
        print("   1. Open http://localhost:3000 to see the AG UI")
        print("   2. Try the suggested prompts in the chat interface")
        print("   3. Test the visualization features")
        print("   4. Monitor the deep agent dashboard")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure the FastAPI backend is running on port 8001")
        print("   2. Check that your Neo4j database is accessible")
        print("   3. Verify your environment variables are set correctly")
        print("   4. Check the backend logs for detailed error messages")

if __name__ == "__main__":
    main()
