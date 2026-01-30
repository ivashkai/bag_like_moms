-- clickhouse/init.sql
CREATE DATABASE IF NOT EXISTS shop_logs;

CREATE TABLE IF NOT EXISTS shop_logs.events (
    ts DateTime64(3),
    event String,
    level String,
    session_id String,
    request_id String,
    ip String,
    user_id Int64,
    payment_id String,
    amount Float64,
    promo_code String,
    already_applied UInt8,
    cart_total Float64,
    latency_ms Int32,
    error_code String,
    bin String,
    search_query String,
    results_count Int32,
    sku String,
    price_at_add Float64,
    price_at_checkout Float64
) ENGINE = MergeTree() ORDER BY ts;