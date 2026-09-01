"""
Monitor Module for simulated OR vital signs.
Generates realistic demo vital signs data for the operating room monitor.
"""

import random
import math
from typing import List, Dict


class ORMonitor:
    """
    Simulated Operating Room Monitor for vital signs.
    Generates medically plausible demo values that vary slightly between requests.
    """
    
    def __init__(self):
        """Initialize monitor with baseline values."""
        self.baseline_hr = 72
        self.baseline_spo2 = 98
        self.baseline_systolic = 120
        self.baseline_diastolic = 80
        self.baseline_rr = 16
        self.baseline_temp = 36.8
        
        # ECG waveform baseline
        self.ecg_frequency = 1.2  # Hz (72 bpm)
        self.time_step = 0
    
    def get_heart_rate(self) -> int:
        """Generate realistic heart rate variation."""
        # Vary HR by ±5 bpm from baseline with slight randomness
        variation = random.randint(-5, 5)
        hr = self.baseline_hr + variation
        return max(40, min(120, hr))  # Keep in medically plausible range
    
    def get_spo2(self) -> int:
        """Generate oxygen saturation."""
        # Vary SpO2 by ±2% from baseline
        variation = random.randint(-2, 2)
        spo2 = self.baseline_spo2 + variation
        return max(90, min(100, spo2))  # Keep in range 90-100%
    
    def get_blood_pressure(self) -> tuple:
        """Generate systolic and diastolic blood pressure."""
        # Vary BP by ±10 systolic, ±5 diastolic
        sys_variation = random.randint(-10, 10)
        dia_variation = random.randint(-5, 5)
        
        systolic = self.baseline_systolic + sys_variation
        diastolic = self.baseline_diastolic + dia_variation
        
        # Ensure diastolic < systolic
        systolic = max(90, min(160, systolic))
        diastolic = max(50, min(systolic - 20, diastolic))
        
        return int(systolic), int(diastolic)
    
    def get_respiratory_rate(self) -> int:
        """Generate respiratory rate."""
        # Vary RR by ±2 from baseline
        variation = random.randint(-2, 2)
        rr = self.baseline_rr + variation
        return max(10, min(30, rr))  # Keep in medically plausible range
    
    def get_temperature(self) -> float:
        """Generate body temperature."""
        # Vary temp by ±0.3°C from baseline
        variation = random.uniform(-0.3, 0.3)
        temp = self.baseline_temp + variation
        return max(36.0, min(38.5, round(temp, 1)))  # Keep in range
    
    def generate_ecg_waveform(self, duration_seconds: float = 5) -> List[Dict]:
        """
        Generate simulated ECG waveform data.
        
        Args:
            duration_seconds: Duration of waveform to generate (default 5 seconds)
        
        Returns:
            List of {time, voltage} points suitable for frontend graphing
        """
        # Sample at 250 Hz (standard ECG sampling rate)
        sample_rate = 250
        num_samples = int(duration_seconds * sample_rate)
        waveform = []
        
        # Use a simple sinusoidal model with some noise for ECG appearance
        for i in range(num_samples):
            time = i / sample_rate
            
            # ECG is roughly sinusoidal at the heart rate frequency
            # Plus some harmonics for PQRST-like appearance
            voltage = (
                1.0 * math.sin(2 * math.pi * self.ecg_frequency * time) +  # Main wave
                0.3 * math.sin(4 * math.pi * self.ecg_frequency * time) +  # Harmonic
                0.1 * math.sin(8 * math.pi * self.ecg_frequency * time) +  # Higher harmonic
                random.uniform(-0.05, 0.05)  # Noise
            )
            
            waveform.append({
                "time": round(time, 3),
                "voltage": round(voltage, 3)
            })
        
        return waveform
    
    def get_full_vitals(self) -> Dict:
        """
        Get complete set of vital signs for the monitor.
        
        Returns:
            Dictionary with all vital signs and ECG data
        """
        hr = self.get_heart_rate()
        spo2 = self.get_spo2()
        systolic, diastolic = self.get_blood_pressure()
        rr = self.get_respiratory_rate()
        temp = self.get_temperature()
        ecg = self.generate_ecg_waveform()
        
        return {
            "simulated": True,
            "timestamp": self._get_timestamp(),
            "vitals": {
                "heart_rate": {
                    "value": hr,
                    "unit": "bpm",
                    "status": "normal" if 60 <= hr <= 100 else "warning"
                },
                "spo2": {
                    "value": spo2,
                    "unit": "%",
                    "status": "normal" if spo2 >= 95 else "warning"
                },
                "systolic_bp": {
                    "value": systolic,
                    "unit": "mmHg",
                    "status": "normal" if 90 <= systolic <= 140 else "warning"
                },
                "diastolic_bp": {
                    "value": diastolic,
                    "unit": "mmHg",
                    "status": "normal" if 50 <= diastolic <= 90 else "warning"
                },
                "respiratory_rate": {
                    "value": rr,
                    "unit": "breaths/min",
                    "status": "normal" if 12 <= rr <= 20 else "warning"
                },
                "temperature": {
                    "value": temp,
                    "unit": "°C",
                    "status": "normal" if 36.5 <= temp <= 37.5 else "warning"
                }
            },
            "ecg": {
                "waveform": ecg,
                "frequency": self.ecg_frequency,
                "sample_rate": 250,
                "unit": "mV"
            },
            "note": "This is simulated demo data and not real clinical measurements."
        }
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


# Global monitor instance
_monitor = ORMonitor()


def get_monitor_vitals() -> Dict:
    """
    Get current vital signs from the OR monitor.
    
    Returns:
        Dictionary with all vital signs
    """
    return _monitor.get_full_vitals()


def reset_monitor() -> Dict:
    """
    Reset the monitor to baseline values.
    
    Returns:
        Confirmation message
    """
    global _monitor
    _monitor = ORMonitor()
    return {
        "success": True,
        "message": "Monitor reset to baseline values",
        "vitals": _monitor.get_full_vitals()
    }
