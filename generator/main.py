import time
import json
import random
import requests
import uuid
from datetime import datetime
import os

# Берем URL из переменной окружения или используем дефолт
VECTOR_URL = os.getenv("VECTOR_URL", "http://vector:8080")


def emit(event_type, data):
    ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')
    payload = {
        "ts": ts,
        "event": event_type,
        "request_id": str(uuid.uuid4()),
        "session_id": str(uuid.uuid4() if 'session_id' not in data else data['session_id']),
        "level": "info",
        **data
    }
    try:
        # Увеличим таймаут
        requests.post(VECTOR_URL, json=payload, timeout=2)
    except Exception as e:
        print(f"Error sending log: {e}")


def simulate():
    print(f"Connecting to Vector at {VECTOR_URL}...")
    # Ждем 5 секунд, пока Vector проснется
    time.sleep(5)

    modes = ['normal', 'peak', 'incident']
    current_mode = 'normal'

    while True:
        if random.random() < 0.1:
            current_mode = random.choice(modes)

        # 1. Аномалия: Orphan Payment
        if random.random() < 0.02:
            emit("payment_succeeded", {"payment_id": str(uuid.uuid4()), "amount": 5000.0})

        # 2. Аномалия: Брутфорс
        if random.random() < 0.05:
            for _ in range(5):
                emit("promo_apply_attempt", {"ip": "192.168.1.105", "promo_code": "HACK_LUCK"})

        # Обычный трафик
        latency = random.randint(50, 200) if current_mode != 'incident' else random.randint(2000, 5000)
        emit("product_view", {"sku": "bag-01", "latency_ms": latency})

        time.sleep(0.1 if current_mode == 'peak' else 0.5)


if __name__ == "__main__":
    simulate()