#!/bin/bash
# crm/cron_jobs/clean_inactive_customers.sh
# Delete customers with no orders in the last year and log how many were deleted.

# Change to the project root (adjust if your manage.py is elsewhere)
cd /absolute/path/to/alx-backend-graphql_crm || exit 1

# Optional: activate virtualenv if you use one (uncomment & edit)
# source /absolute/path/to/venv/bin/activate

# Use Django manage.py shell to perform deletion and print the count
deleted_count=$(python3 manage.py shell -c "
from django.utils import timezone
from datetime import timedelta

# Adjust imports below if your models are in a different module.
try:
    from crm.models import Customer, Order
except Exception:
    # If your Order relation name or module differs, change above import accordingly.
    raise

one_year_ago = timezone.now() - timedelta(days=365)

# NOTE: this assumes the related name on Order -> Customer is 'order' (order__date).
# If your relation is Order.customer (default), Django will use 'order' or 'order_set' - adjust if needed.
inactive_customers = Customer.objects.exclude(order__date__gte=one_year_ago).distinct()
count = inactive_customers.count()
inactive_customers.delete()
print(count)
" 2>/dev/null)

# In case the python command printed nothing, set to 0
deleted_count=${deleted_count:-0}

# Log with timestamp
printf "[%s] Deleted customers: %s\n" "$(date '+%Y-%m-%d %H:%M:%S %Z')" "$deleted_count" >> /tmp/customer_cleanup_log.txt
