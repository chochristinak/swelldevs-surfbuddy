#-------------------- Module Imports --------------------
from django.apps import AppConfig

#-------------------- Config --------------------
# Main App Config
class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'
