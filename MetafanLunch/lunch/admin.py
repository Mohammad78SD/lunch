from django.contrib import admin
from lunch.models import Lunch, CustomUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import jdatetime
from django.contrib.auth.models import Group
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class ShamsiDateRangeFilter(admin.SimpleListFilter):
    title = _("تاریخ ماهانه")
    parameter_name = "shamsi_date_range"

    def lookups(self, request, model_admin):
        return (("current", _("ماه جاری")),)

    def queryset(self, request, queryset):
        if self.value() == "current":
            today = timezone.now().date()
            j_today = jdatetime.date.fromgregorian(date=today)

            # Calculate start and end dates for the current Shamsi month range
            if j_today.month == 1:
                start_date_jalali = jdatetime.date(j_today.year - 1, 12, 25)
            else:
                start_date_jalali = jdatetime.date(j_today.year, j_today.month - 1, 25)

            end_date_jalali = jdatetime.date(j_today.year, j_today.month, 25)

            print(start_date_jalali, end_date_jalali)
            return queryset.filter(date__range=(start_date_jalali, end_date_jalali))

        return queryset


class Filter(admin.ModelAdmin):
    list_display = ("user_name", "dates")
    list_filter = ("user", ShamsiDateRangeFilter, "date")

    def user_name(self, obj):
        return obj.user

    def dates(self, obj):
        return obj.date

    user_name.short_description = "کاربر"
    dates.short_description = "تاریخ"


admin.site.register(Lunch, Filter)


class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("phone_number", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (
            "مشخصات فردی",
            {
                "fields": (
                    "avatar",
                    "first_name",
                    "last_name",
                    "father_name",
                    "birthdate",
                    "national_code",
                    "address",
                    "postal_code",
                    "description",
                )
            },
        ),
        ("سابقه کاربر", {"fields": ("education", "major", "start_date", "end_date")}),
        ("Permissions", {"fields": ("is_file", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("phone_number",)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.unregister(Group)
