import os
import sys
import django

# Указываете путь к вашему проекту (где находится файл manage.py)
DJANGO_PROJECT_PATH = 'C:/Users/enft/Desktop/dbdit'

# Добавляете путь к проекту в sys.path
sys.path.append(DJANGO_PROJECT_PATH)

# Устанавливаете переменную окружения DJANGO_SETTINGS_MODULE
os.environ['DJANGO_SETTINGS_MODULE'] = 'ditdb.settings'

# Инициализируете Django
django.setup()

# Ваши остальные импорты и код
from directories.models import *


users = SkladyOffice.objects.all()

for user in users:
    user.sklad_name_lower = user.sklad_name.lower()
    try:
        user.save()
    except Exception as e:
        print(f"Error saving user {user.sklad_name}: {e}")