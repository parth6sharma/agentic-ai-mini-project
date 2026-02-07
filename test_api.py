"""
Test script for the Multi-Agent Weather System
Demonstrates the workflow and agent communication
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"


def test_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint and print results."""
    print(f"\n{'='*70}")
    print(f"Testing: {method} {endpoint}")
    print(f"{'='*70}")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        else:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("MULTI-AGENT WEATHER SYSTEM - TEST SUITE")
    print("="*70)
    
    # Wait for server to be ready
    print("\nWaiting for server to start...")
    time.sleep(2)
    
    # Test 1: Root endpoint
    test_endpoint("/")
    
    # Test 2: Health check
    test_endpoint("/health")
    
    # Test 3: Weather request with summary (2 tasks)
    test_endpoint(
        "/process",
        method="POST",
        data={"request": "Get the current weather in New York and give me a short summary."}
    )
    
    # Test 4: Weather request for different city with summary
    test_endpoint(
        "/process",
        method="POST",
        data={"request": "What's the weather in London and summarize it"}
    )
    
    # Test 5: Simple weather request without summary (1 task)
    test_endpoint(
        "/process",
        method="POST",
        data={"request": "Get weather for Tokyo"}
    )
    
    # Test 6: Another city
    test_endpoint(
        "/process",
        method="POST",
        data={"request": "Tell me the weather in Paris and give me a summary"}
    )
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED!")
    print("="*70)
    print("\nAgent Communication Flow Demonstrated:")
    print("1. User makes request to FastAPI server")
    print("2. Server forwards request to Agent A")
    print("3. Agent A breaks down request into tasks:")
    print("   - Task 1: Get weather data (executed by Agent B)")
    print("   - Task 2: Summarize data (executed by Agent B)")
    print("4. Agent B executes each task sequentially")
    print("5. Agent A compiles results and returns final response")
    print("6. Server returns response to user")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
