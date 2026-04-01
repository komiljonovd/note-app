from django.apps import AppConfig


class NoteappConfig(AppConfig):
    name = 'noteapp'

    def ready(self):
        import noteapp.signals
