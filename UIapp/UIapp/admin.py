from django.contrib import admin
from models import *


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)


class Category_valueAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category_value, Category_valueAdmin)


class QueryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Query, QueryAdmin)


class ResultsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Results, ResultsAdmin)


class Query_propertiesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Query_properties, ResultsAdmin)

class TeamAdmin(admin.ModelAdmin):
    pass


admin.site.register(Team, ResultsAdmin)

class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ResultsAdmin)
