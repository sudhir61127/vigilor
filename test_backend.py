"""
Test script for VIGIL-OR backend API
"""
import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing /health ===")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/health")
        data = json.loads(response.read().decode())
        print(f"✓ Health: {data}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_agent_patient():
    """Test agent endpoint with patient query"""
    print("\n=== Testing /agent (Patient Query) ===")
    try:
        data = json.dumps({"user_input": "Show patient P001"}).encode()
        request = urllib.request.Request(
            f"{BASE_URL}/agent",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        response = urllib.request.urlopen(request)
        result = json.loads(response.read().decode())
        print(f"✓ Intent: {result.get('intent', 'unknown')}")
        print(f"✓ Response preview: {result.get('response', 'No response')[:200]}...")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_agent_report():
    """Test agent endpoint with report query"""
    print("\n=== Testing /agent (Report Query) ===")
    try:
        data = json.dumps({"user_input": "Show MRI report for P001"}).encode()
        request = urllib.request.Request(
            f"{BASE_URL}/agent",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        response = urllib.request.urlopen(request)
        result = json.loads(response.read().decode())
        print(f"✓ Intent: {result.get('intent', 'unknown')}")
        print(f"✓ Response preview: {result.get('response', 'No response')[:200]}...")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_monitor():
    """Test monitor endpoint"""
    print("\n=== Testing /monitor ===")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/monitor")
        data = json.loads(response.read().decode())
        print(f"✓ Simulated: {data.get('simulated', 'N/A')}")
        print(f"✓ Heart Rate: {data.get('vitals', {}).get('heart_rate', {}).get('value', 'N/A')}")
        print(f"✓ SpO2: {data.get('vitals', {}).get('spo2', {}).get('value', 'N/A')}")
        print(f"✓ ECG waveform points: {len(data.get('ecg', {}).get('waveform', []))}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_agent_checklist():
    """Test agent endpoint with checklist query"""
    print("\n=== Testing /agent (Checklist Query) ===")
    try:
        data = json.dumps({"user_input": "Show surgical checklist"}).encode()
        request = urllib.request.Request(
            f"{BASE_URL}/agent",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        response = urllib.request.urlopen(request)
        result = json.loads(response.read().decode())
        print(f"✓ Intent: {result.get('intent', 'unknown')}")
        print(f"✓ Response preview: {result.get('response', 'No response')[:200]}...")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("VIGIL-OR Backend API Tests")
    print("=" * 60)
    
    results = []
    results.append(("Health", test_health()))
    results.append(("Agent - Patient", test_agent_patient()))
    results.append(("Agent - Report", test_agent_report()))
    results.append(("Monitor", test_monitor()))
    results.append(("Agent - Checklist", test_agent_checklist()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)
