from django.contrib import admin

from apps.applicant.models import Applicant


class ApplicantAdmin(admin.ModelAdmin):
    model = Applicant

    list_display = ("first_name", "last_name", "email", "phone", "gender", "country", 'created_at',)
    search_fields = ("first_name", "last_name", "email")
    ordering = ('-created_at', "gender", "country")


admin.site.register(Applicant, ApplicantAdmin)
