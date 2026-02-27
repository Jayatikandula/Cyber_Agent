import random
from datetime import datetime

def calculate_risk():
    sophistication = random.randint(1,5)
    sensitivity = random.randint(1,5)
    spread = random.randint(1,5)
    impact = random.randint(1,5)
    exploit = random.randint(1,5)

    score = sophistication + sensitivity + spread + impact + exploit

    if score <= 8:
        level = "Low"
    elif score <= 15:
        level = "Medium"
    elif score <= 20:
        level = "High"
    else:
        level = "Critical"

    return {
        "score": score,
        "level": level,
        "timestamp": datetime.now()
    }