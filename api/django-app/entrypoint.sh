#!/bin/sh
set -e


echo "⏳ Waiting for Redis..."
until nc -z redis 6379; do
  echo "   Redis is unavailable - sleeping"
  sleep 1
done
echo "✅ Redis is up!"

echo "⏳ Waiting for MinIO..."
until nc -z 161.97.104.181 80; do
  echo "   MinIO is unavailable - sleeping"
  sleep 1
done
echo "✅ MinIO is up!"

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

echo "🔄 Collecting static files..."
python manage.py collectstatic --noinput || echo "⚠️  Static collection failed, continuing..."

echo "👤 Creating superuser if not exists..."
python manage.py shell << END
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_ADMIN_USERNAME', 'admin')
email = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✅ Superuser "{username}" created')
else:
    print(f'⚠️  Superuser "{username}" already exists')
END

echo "🚀 Starting Django development server..."
exec "$@"
