from django.contrib import admin
from apps.common.secret_note.models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'access_token', 'is_viewed', 'timestamp')