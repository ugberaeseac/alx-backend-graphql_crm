#!/bin/bash

# Schedule a customer clean up script

cd /home/ugberaeseac/alx-backend-graphql_crm/ || exit
source venv/bin/activate

DELETED_CUSTOMERS=$(python3 manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
customer = Customer.objects.filter(orders__isnull=True, created_at__lte=one_year_ago)

count = customer.count()
customer.delete()
print(count)
")

echo \"\$(date '+%Y-%m-%d %H:%M:%S') - \$DELETED_CUSTOMERS inactive customers deleted\" >> /tmp/customer_cleanup_log.txt