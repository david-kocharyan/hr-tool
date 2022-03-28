from django.contrib import admin

from apps.company.models import Company


class CompanyAdmin(admin.ModelAdmin):
    model = Company
    prepopulated_fields = {'slug': ('name',)}

    list_display = ('name', 'owner', 'industry', 'address', 'contacts',)
    search_fields = ('name', 'industry')
    ordering = ('-created_at',)


admin.site.register(Company, CompanyAdmin)
