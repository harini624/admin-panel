
from django.contrib import admin, messages
from .models import Properties, PropertyImage
from .property_sync import sync_property


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]

    def save_related(self, request, form, formsets, change):
        # Save gallery images first, then synchronize the complete property.
        super().save_related(request, form, formsets, change)

        try:
            result = sync_property(form.instance)
            messages.success(
                request,
                "Property synchronized with the customer website."
            )
        except Exception as exc:
            messages.error(
                request,
                "Property saved locally, but synchronization failed. "
                "Check that the receiver is running and its API token "
                "matches the sender. Error: {}".format(exc)
            )


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "image_type")
