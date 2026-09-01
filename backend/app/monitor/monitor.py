from random import uniform


def get_system_status():
    return {
        "temperature": round(uniform(35, 45), 2),
        "pressure": round(uniform(95, 105), 2),
        "vibration": round(uniform(0.1, 0.5), 2),
        "power": round(uniform(80, 100), 2),
    }