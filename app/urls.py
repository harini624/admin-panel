from django.urls import path
from . import views

urlpatterns = [

    path(
        "submit_properties/",
        views.submit_properties,
        name="submit_properties"
    ),

    path(
        "update_property/<int:id>/",
        views.update_property,
        name="update_property"
    ),

    path(
        "delete_property/<int:id>/",
        views.delete_property,
        name="delete_property"
    ),

    path(
        "publish_property/<int:id>/",
        views.publish_property,
        name="publish_property"
    ),

    path(
        "unpublish_property/<int:id>/",
        views.unpublish_property,
        name="unpublish_property"
    ),

    path(
        "make_unavailable/<int:id>/",
        views.make_unavailable,
        name="make_unavailable"
    ),

    path(
        "make_available/<int:id>/",
        views.make_available,
        name="make_available"
    ),

    path(
        "api/properties/",
        views.client_properties_api,
        name="client_properties_api"
    ),

    path(
        "api/properties/<int:id>/",
        views.client_property_detail_api,
        name="client_property_detail_api"
    ),
]