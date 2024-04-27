from django.apps import AppConfig

from .yolo5detect import Yolo5Detect

class HelmetdetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HelmetDetection'

    def ready(self) -> None:
        HelmetdetectionConfig.y5d = Yolo5Detect()
        return super().ready()