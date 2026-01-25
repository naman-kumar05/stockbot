"""
Test script for StockBot API
Run this to verify all components are working correctly.
"""

import requests
import json
import time
import sys
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except:
        pass

API_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Is the backend server running?")
        print("   Start it with: uvicorn api.main:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_chat(message: str):
    """Test chat endpoint."""
    print(f"\n💬 Testing chat with message: '{message}'")
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": message},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat request successful!")
            print(f"\n📝 Response:")
            print("-" * 60)
            print(data.get("reply", "No reply in response"))
            print("-" * 60)
            
            meta = data.get("meta", {})
            if meta:
                print(f"\n📊 Metadata:")
                print(f"   Company: {meta.get('company', 'N/A')}")
                print(f"   Ticker: {meta.get('ticker', 'N/A')}")
                print(f"   Intent: {meta.get('intent', 'N/A')}")
                if meta.get('chart'):
                    print(f"   Chart: Available ✅")
            
            return True
        else:
            print(f"❌ Chat request failed: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out (took > 30 seconds)")
        return False
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return False

def test_clear_history():
    """Test clear history endpoint."""
    print("\n🗑️  Testing clear history...")
    try:
        response = requests.post(
            f"{API_URL}/clear-history",
            json={},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Clear history successful!")
            return True
        else:
            print(f"❌ Clear history failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Clear history error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 StockBot API Test Suite")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Backend server is not running. Please start it first.")
        print("   Command: uvicorn api.main:app --reload --port 8000")
        print("   (Run from project root directory)")
        sys.exit(1)
    
    # Test 2: Basic chat
    test_messages = [
        "What's the price of Apple?",
        "Tell me about Tesla",
        "Should I invest in Microsoft?"
    ]
    
    print("\n" + "=" * 60)
    print("📝 Running Chat Tests")
    print("=" * 60)
    
    for msg in test_messages:
        test_chat(msg)
        time.sleep(2)  # Small delay between requests
    
    # Test 3: Clear history
    test_clear_history()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\n💡 Tips:")
    print("   - Check the UI at http://localhost:8501 for visual testing")
    print("   - Try different stock questions to test adaptability")
    print("   - Check backend logs for any errors")

if __name__ == "__main__":
    main()
