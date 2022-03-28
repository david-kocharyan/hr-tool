from django.contrib import admin

from apps.position.models import Position


class PositionAdmin(admin.ModelAdmin):
    model = Position

    list_display = ('name', 'skill', 'number', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


admin.site.register(Position, PositionAdmin)
