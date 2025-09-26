from django.contrib import admin

# Register your models here.

from .models import Season, Category, Player, MatchParticipation, Match

admin.site.register(Season)
admin.site.register(Category)
admin.site.register(Player)
admin.site.register(MatchParticipation)
admin.site.register(Match)
