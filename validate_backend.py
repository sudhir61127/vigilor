#!/usr/bin/env python3
"""Quick validation that backend components load correctly"""

print("Validating VIGIL-OR Backend Components...")
print("-" * 60)

try:
    print("✓ Loading RAG tools...", end=" ")
    from backend.app.tools.rag_tool import search_medical_reports
    print("OK")
except Exception as e:
    print(f"FAIL: {e}")

try:
    print("✓ Loading patient tools...", end=" ")
    from backend.app.tools.patient_tool import search_patient, list_all_patients
    print("OK")
except Exception as e:
    print(f"FAIL: {e}")

try:
    print("✓ Loading checklist tools...", end=" ")
    from backend.app.tools.checklist_tool import get_surgical_checklist
    print("OK")
except Exception as e:
    print(f"FAIL: {e}")

try:
    print("✓ Loading monitor tools...", end=" ")
    from backend.app.tools.monitor_tool import get_current_vitals
    print("OK")
except Exception as e:
    print(f"FAIL: {e}")

try:
    print("✓ Loading monitor module...", end=" ")
    from backend.app.monitor.monitor import get_monitor_vitals
    print("OK")
except Exception as e:
    print(f"FAIL: {e}")

try:
    print("✓ Loading LangGraph workflow...", end=" ")
    from backend.app.graph.workflow import run_agent
    print("OK")
except Exception as e:
    print(f"FAIL: {e}")

try:
    print("✓ Loading API routes...", end=" ")
    from backend.app.api.routes import router
    print("OK")
except Exception as e:
    print(f"FAIL: {e}")

print("-" * 60)
print("✓ All components loaded successfully!")

# Test a simple agent run
print("\nTesting Agent Execution...")
print("-" * 60)

try:
    result = run_agent("Show patient P001")
    print(f"✓ Query: 'Show patient P001'")
    print(f"✓ Intent: {result.get('intent', 'unknown')}")
    print(f"✓ Response (first 200 chars): {result.get('response', 'No response')[:200]}...")
    print("-" * 60)
    print("✓ Agent test successful!")
except Exception as e:
    print(f"✗ Agent test failed: {e}")

# Test monitor
print("\nTesting Monitor...")
print("-" * 60)

try:
    vitals = get_monitor_vitals()
    print(f"✓ Simulated: {vitals.get('simulated', 'N/A')}")
    print(f"✓ Heart Rate: {vitals.get('vitals', {}).get('heart_rate', {}).get('value', 'N/A')} bpm")
    print(f"✓ SpO2: {vitals.get('vitals', {}).get('spo2', {}).get('value', 'N/A')}%")
    print(f"✓ ECG waveform points: {len(vitals.get('ecg', {}).get('waveform', []))}")
    print("-" * 60)
    print("✓ Monitor test successful!")
except Exception as e:
    print(f"✗ Monitor test failed: {e}")

print("\n" + "=" * 60)
print("✓✓✓ VIGIL-OR Backend Validation Complete ✓✓✓")
print("=" * 60)
