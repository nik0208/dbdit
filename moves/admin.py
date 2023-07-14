from django.apps import apps
from django.contrib import admin

# Получаем список всех моделей
app_models = apps.get_app_config('moves').get_models()

# Регистрируем каждую модель
for model in app_models:
    admin.site.register(model)