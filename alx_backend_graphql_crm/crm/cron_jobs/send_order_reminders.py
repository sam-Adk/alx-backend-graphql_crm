#!/usr/bin/env python3
"""
send_order_reminders.py
Fetch orders made within the last 7 days using GraphQL and log reminders.
"""

import requests
from datetime import datetime, timedelta

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Calculate 7 days ago
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# GraphQL query to fetch recent orders
query = """
query GetRecentOrders($date: Date!) {
  orders(filter: { orderDate_Gte: $date }) {
    id
    customer {
      email
    }
  }
}
"""

# Send the POST request to GraphQL
try:
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": {"date": seven_days_ago}},
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    response.raise_for_status()
    data = response.json()
except Exception as e:
    with open("/tmp/order_reminders_log.txt", "a") as f:
        f.write(f"[{datetime.now()}] Error fetching orders: {e}\n")
    exit(1)

# Extract order data
orders = data.get("data", {}).get("orders", [])

# Log each order reminder
with open("/tmp/order_reminders_log.txt", "a") as f:
    f.write(f"\n[{datetime.now()}] --- Order Reminder Log ---\n")
    if orders:
        for order in orders:
            order_id = order.get("id")
            customer_email = order.get("customer", {}).get("email")
            f.write(f"Order ID: {order_id}, Customer Email: {customer_email}\n")
    else:
        f.write("No recent orders found.\n")

print("Order reminders processed!")
