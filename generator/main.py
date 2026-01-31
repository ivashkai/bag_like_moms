import pika
import json
import time
import random
import uuid

params = pika.ConnectionParameters(host='rabbitmq', heartbeat=600)


def generate_shop_event():
    event_type = random.choices(
        ["view", "add_to_cart", "payment", "promo_error", "critical_bug"],
        weights=[60, 20, 10, 7, 3]
    )[0]

    # ,fpf
    data = {
        "shop": "bag_like_moms",
        "event": event_type,
        "session_id": str(uuid.uuid4()),
        "sku": f"bag-{random.randint(1, 15)}",
        "price": float(random.randint(1000, 15000)),
        "latency_ms": random.uniform(50, 200)
    }

    # аномалии
    log_msg = "User action processed"
    level = "INFO"

    if event_type == "promo_error":
        data["promo_code"] = "MOM_SALE_2026"
        data["error_code"] = "already_applied"
        level = "WARN"
        log_msg = "Double promo code attempt detected"

    elif event_type == "critical_bug":
        data["cart_total"] = -100.0  # Отрицательная цена
        level = "ERROR"
        log_msg = "Negative cart total detected! Integrity breach."

    elif event_type == "payment" and random.random() < 0.2:
        level = "ERROR"
        log_msg = "Payment gateway timeout"
        data["latency_ms"] = random.uniform(3000, 5000)

    return {
        "metrics": {
            "price": data["price"],
            "latency": data["latency_ms"],
            "is_error": 1 if level == "ERROR" else 0
        },
        "log": {
            "level": level,
            "event": event_type,
            "msg": log_msg,
            "sku": data["sku"]
        }
    }


def main():
    while True:
        try:
            conn = pika.BlockingConnection(params)
            ch = conn.channel()
            ch.queue_declare(queue='events', durable=True)
            while True:
                payload = generate_shop_event()
                ch.basic_publish(exchange='', routing_key='events', body=json.dumps(payload))
                print(f" [x] Sent {payload['log']['event']} | Level: {payload['log']['level']}")
                time.sleep(0.5)
        except Exception as e:
            print(f"Conn error: {e}. Retry in 5s...")
            time.sleep(5)


if __name__ == "__main__":
    main()