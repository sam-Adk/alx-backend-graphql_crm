import datetime

def log_crm_heartbeat():
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{now} CRM is alive\n"

    # Append the message to the log file
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)

    print("Heartbeat logged successfully!")
import datetime
import requests

def update_low_stock():
    url = "http://localhost:8000/graphql"
    query = """
    mutation {
      updateLowStockProducts {
        message
        updatedProducts {
          name
          stock
        }
      }
    }
    """

    response = requests.post(url, json={'query': query})
    data = response.json()

    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file = "/tmp/low_stock_updates_log.txt"

    with open(log_file, "a") as f:
        f.write(f"\n[{now}] Low Stock Update Triggered\n")
        if "data" in data and data["data"]["updateLowStockProducts"]:
            result = data["data"]["updateLowStockProducts"]
            f.write(f"Message: {result['message']}\n")
            for p in result["updatedProducts"]:
                f.write(f"- {p['name']} → Stock: {p['stock']}\n")
        else:
            f.write("Error: No data returned from GraphQL endpoint\n")

    print("Low-stock update job executed.")
