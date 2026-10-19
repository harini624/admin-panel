from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
import requests
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST


from app.models import Properties, PropertyImage


# =========================================================
# ADMIN PROPERTY PAGE
# =========================================================


def submit_properties(request):

    if request.method == "POST":

        furnished = request.POST.get("furnished")
        location = request.POST.get("location")
        price = request.POST.get("price")
        bhk = request.POST.get("bhk")
        contact = request.POST.get("contact")

        hall_image = request.FILES.get("hall_image")

        # Create the property first.
        property = Properties.objects.create(
            furnished=furnished,
            location=location,
            price=price,
            bhk=bhk,
            contact=contact,
            hall_image=hall_image,
            published=False,
            available=True
        )

        # Save bedroom images.
        bedroom_images = request.FILES.getlist("bedroom_image")

        for image in bedroom_images:
            PropertyImage.objects.create(
                property=property,
                image=image,
                image_type="bedroom"
            )

        # Save bathroom images.
        bathroom_images = request.FILES.getlist("bathroom_image")

        for image in bathroom_images:
            PropertyImage.objects.create(
                property=property,
                image=image,
                image_type="bathroom"
            )

        # Save kitchen images.
        kitchen_images = request.FILES.getlist("kitchen_image")

        for image in kitchen_images:
            PropertyImage.objects.create(
                property=property,
                image=image,
                image_type="kitchen"
            )

        # Save balcony images.
        balcony_images = request.FILES.getlist("balcony_image")

        for image in balcony_images:
            PropertyImage.objects.create(
                property=property,
                image=image,
                image_type="balcony"
            )

        # DEBUG: verify that all images were received and saved.
        print("\n========== PROPERTY IMAGE DEBUG ==========")
        print("Property ID:", property.id)
        print("Uploaded file fields:", list(request.FILES.keys()))
        print("Bedroom images received:", len(bedroom_images))
        print("Bathroom images received:", len(bathroom_images))
        print("Kitchen images received:", len(kitchen_images))
        print("Balcony images received:", len(balcony_images))
        print("Total gallery images saved:", property.images.count())

        for saved_image in property.images.all():
            print(
                "Saved image:",
                saved_image.image.name,
                "| Type:",
                saved_image.image_type
            )

        print("==========================================\n")

        messages.success(
            request,
            "Property and gallery images saved successfully."
        )

        return redirect("submit_properties")

    # SEARCH
    search = request.GET.get("search", "")

    properties = Properties.objects.all().order_by("-id")

    if search:
        properties = properties.filter(
            Q(furnished__icontains=search) |
            Q(location__icontains=search) |
            Q(contact__icontains=search)
        )

    # FILTER
    status = request.GET.get("status", "")

    if status == "available":
        properties = properties.filter(available=True)

    elif status == "unavailable":
        properties = properties.filter(available=False)

    elif status == "published":
        properties = properties.filter(published=True)

    elif status == "unpublished":
        properties = properties.filter(published=False)

    # DASHBOARD COUNTS
    total_properties = Properties.objects.count()

    published_count = Properties.objects.filter(
        published=True
    ).count()

    available_count = Properties.objects.filter(
        available=True
    ).count()

    return render(
        request,
        "submit_properties.html",
        {
            "properties": properties,
            "search": search,
            "status": status,
            "total_properties": total_properties,
            "published_count": published_count,
            "available_count": available_count,
        }
    )

def update_property(request, id):

    property = get_object_or_404(Properties, id=id)

    if request.method == "POST":

        # =====================================================
        # UPDATE PROPERTY DETAILS
        # =====================================================

        property.furnished = request.POST.get("furnished")
        property.location = request.POST.get("location")
        property.price = request.POST.get("price")
        property.bhk = request.POST.get("bhk")
        property.contact = request.POST.get("contact")

        # =====================================================
        # AVAILABILITY
        # =====================================================

        available = request.POST.get("available")

        if available == "True":
            property.available = True
        else:
            property.available = False


        # =====================================================
        # REPLACE MAIN HALL IMAGE
        # =====================================================

        hall_image_replace = request.FILES.get("hall_image_replace")

        if hall_image_replace:
            property.hall_image = hall_image_replace


        # =====================================================
        # DELETE MAIN HALL IMAGE
        # =====================================================

        delete_hall = request.POST.get("delete_hall")

        if delete_hall == "true":
            property.hall_image = None


        # Save property changes
        property.save()


        # =====================================================
        # ADD ADDITIONAL HALL IMAGES
        # =====================================================

        hall_images = request.FILES.getlist("hall_images")

        print("ADDITIONAL HALL IMAGES:", hall_images)

        for image in hall_images:

            PropertyImage.objects.create(
                property=property,
                image=image,
                image_type="hall"
            )


        # =====================================================
        # REPLACE EXISTING EXTRA IMAGES
        # =====================================================

        for existing_image in property.images.all():

            replacement_image = request.FILES.get(
                f"replace_image_{existing_image.id}"
            )

            if replacement_image:

                existing_image.image = replacement_image
                existing_image.save()


        # =====================================================
        # DELETE EXISTING EXTRA IMAGE
        # =====================================================

        delete_image_id = request.POST.get("delete_image")

        if delete_image_id:

            image_to_delete = get_object_or_404(
                PropertyImage,
                id=delete_image_id,
                property=property
            )

            image_to_delete.delete()


        # =====================================================
        # ADD BEDROOM IMAGES
        # =====================================================

        bedroom_images = request.FILES.getlist("bedroom_image")

        for image in bedroom_images:

            PropertyImage.objects.create(
                property=property,
                image=image,
                image_type="bedroom"
            )


        # =====================================================
        # ADD BATHROOM IMAGES
        # =====================================================

        bathroom_images = request.FILES.getlist("bathroom_image")

        for image in bathroom_images:

            PropertyImage.objects.create(
                property=property,
                image=image,
                image_type="bathroom"
            )


        # =====================================================
        # ADD KITCHEN IMAGES
        # =====================================================

        kitchen_images = request.FILES.getlist("kitchen_image")

        for image in kitchen_images:

            PropertyImage.objects.create(
                property=property,
                image=image,
                image_type="kitchen"
            )


        # =====================================================
        # ADD BALCONY IMAGES
        # =====================================================

        balcony_images = request.FILES.getlist("balcony_image")

        for image in balcony_images:

            PropertyImage.objects.create(
                property=property,
                image=image,
                image_type="balcony"
            )


        # =====================================================
        # FINISH
        # =====================================================

        return redirect(
            "update_property",
            id=property.id
        )


    # =========================================================
    # GET REQUEST
    # =========================================================

    return render(
        request,
        "update_properties.html",
        {
            "property": property
        }
    )
# =========================================================
# DELETE PROPERTY
# =========================================================

def delete_property(request, id):

    property = get_object_or_404(
        Properties,
        id=id
    )

    if request.method == "POST":

        property.delete()

    return redirect("submit_properties")


# =========================================================
# PUBLISH PROPERTY

@require_POST
def publish_property(request, id):
    property_obj = get_object_or_404(Properties, id=id)

    if not property_obj.available:
        messages.error(
            request,
            "This property is unavailable and cannot be published."
        )
        return redirect("submit_properties")

    api_url = settings.CLIENT_WEBSITE_API_URL
    api_token = settings.RECEIVE_PROPERTY_API_TOKEN

    property_data = {
        "source_property_id": str(property_obj.id),
        "furnished": property_obj.furnished,
        "location": property_obj.location,
        "price": str(property_obj.price),
        "bhk": str(property_obj.bhk),
        "contact": property_obj.contact,
        "published": "true",
        "available": str(property_obj.available).lower(),
    }

    files = {}
    opened_files = []

    try:
        # Send the main images.
        for field_name in ("house_image", "hall_image"):
            image_field = getattr(property_obj, field_name, None)

            if image_field and image_field.name:
                image_file = image_field.open("rb")
                opened_files.append(image_file)

                files[field_name] = (
                    image_field.name.split("/")[-1],
                    image_file,
                    "application/octet-stream",
                )

        # Send all gallery images, starting from index 0.
        for index, gallery_image in enumerate(
            property_obj.images.all()
        ):
            image_field = gallery_image.image

            if image_field and image_field.name:
                image_file = image_field.open("rb")
                opened_files.append(image_file)

                files["gallery_{}".format(index)] = (
                    image_field.name.split("/")[-1],
                    image_file,
                    "application/octet-stream",
                )

                # Send the image type as ordinary POST data.
                property_data["gallery_type_{}".format(index)] = (
                    gallery_image.image_type or "gallery"
                )

        response = requests.post(
            api_url,
            data=property_data,
            files=files or None,
            headers={
                "Authorization": "Bearer " + api_token
            },
            timeout=20,
        )

        print("DEBUG: Receiver status:", response.status_code)
        print("DEBUG: Receiver response:", response.text)

        response.raise_for_status()

        property_obj.published = True
        property_obj.save(update_fields=["published"])

        messages.success(
            request,
            "Property published to the client website successfully."
        )

    except requests.RequestException as exc:
        print("DEBUG: Publish request failed:", str(exc))
        messages.error(
            request,
            "Publishing failed. Please check the client website API."
        )

    finally:
        for image_file in opened_files:
            image_file.close()

    return redirect("submit_properties")



# =========================================================
# UNPUBLISH PROPERTY
# =========================================================

def unpublish_property(request, id):

    property = get_object_or_404(
        Properties,
        id=id
    )

    if request.method == "POST":

        property.published = False

        property.save()

    return redirect("submit_properties")


# =========================================================
# MAKE PROPERTY AVAILABLE / UNAVAILABLE
# =========================================================

def toggle_availability(request, id):

    property = get_object_or_404(
        Properties,
        id=id
    )

    if request.method == "POST":

        property.available = not property.available

        property.save()

    return redirect("submit_properties")


# =========================================================
# CLIENT API
# =========================================================

def client_properties_api(request):

    properties = Properties.objects.filter(
        published=True,
        available=True
    ).prefetch_related("images")

    data = []

    for property in properties:
        hall_images = []
        bedroom_images = []
        bathroom_images = []
        kitchen_images = []
        balcony_images = []

        for image in property.images.all():

            image_url = request.build_absolute_uri(
                image.image.url
            )
            if image.image_type == "hall":

                    hall_images.append(image_url)
            elif image.image_type == "bedroom":

                bedroom_images.append(image_url)

            elif image.image_type == "bathroom":

                bathroom_images.append(image_url)

            elif image.image_type == "kitchen":

                kitchen_images.append(image_url)

            elif image.image_type == "balcony":

                balcony_images.append(image_url)

        property_data = {

            "id": property.id,

            "furnished": property.furnished,

            "location": property.location,

            "price": str(property.price),

            "bhk": property.bhk,

            "contact": property.contact,

            "house_image": (
                request.build_absolute_uri(
                    property.house_image.url
                )
                if property.house_image
                else None
            ),

            "hall_image": (
    request.build_absolute_uri(
        property.hall_image.url
    )
    if property.hall_image
    else None
),

"hall_images": hall_images,

"bedroom_images": bedroom_images,

            "bathroom_images": bathroom_images,

            "kitchen_images": kitchen_images,

            "balcony_images": balcony_images,

            "published": property.published,

            "available": property.available
        }

        data.append(property_data)

    return JsonResponse(
        {
            "success": True,
            "count": len(data),
            "properties": data
        }
    )


# =========================================================
# SINGLE CLIENT PROPERTY API
# =========================================================

def client_property_detail_api(request, id):

    property = get_object_or_404(
        Properties,
        id=id,
        published=True,
        available=True
    )

    bedroom_images = []
    bathroom_images = []
    kitchen_images = []
    balcony_images = []

    for image in property.images.all():

        image_url = request.build_absolute_uri(
            image.image.url
        )

        if image.image_type == "bedroom":

            bedroom_images.append(image_url)

        elif image.image_type == "bathroom":

            bathroom_images.append(image_url)

        elif image.image_type == "kitchen":

            kitchen_images.append(image_url)

        elif image.image_type == "balcony":

            balcony_images.append(image_url)

    data = {

        "id": property.id,

        "furnished": property.furnished,

        "location": property.location,

        "price": str(property.price),

        "bhk": property.bhk,

        "contact": property.contact,

        "house_image": (
            request.build_absolute_uri(
                property.house_image.url
            )
            if property.house_image
            else None
        ),

        "hall_image": (
            request.build_absolute_uri(
                property.hall_image.url
            )
            if property.hall_image
            else None
        ),

        "bedroom_images": bedroom_images,

        "bathroom_images": bathroom_images,

        "kitchen_images": kitchen_images,

        "balcony_images": balcony_images,

        "published": property.published,

        "available": property.available
    }

    return JsonResponse(
        {
            "success": True,
            "property": data
        }
    )


# =========================================================
# MAKE UNAVAILABLE
# =========================================================

def make_unavailable(request, id):

    property = get_object_or_404(
        Properties,
        id=id
    )

    property.available = False

    property.save()

    return redirect("submit_properties")


# =========================================================
# MAKE AVAILABLE
# =========================================================

def make_available(request, id):

    property = get_object_or_404(
        Properties,
        id=id
    )

    property.available = True

    property.save()

    return redirect("submit_properties")

def sync_property_status(property_obj):
    api_url = settings.CLIENT_WEBSITE_STATUS_API_URL
    api_token = settings.RECEIVE_PROPERTY_API_TOKEN

    data = {
        "source_property_id": str(property_obj.id),
        "available": str(property_obj.available).lower(),
        "published": str(property_obj.published).lower(),
    }

    try:
        response = requests.post(
            api_url,
            data=data,
            headers={
                "Authorization": "Bearer " + api_token
            },
            timeout=20,
        )

        response.raise_for_status()

        result = response.json()

        if not result.get("success"):
            print("Status sync was not confirmed:", result)
            return False

        print("Property status synchronized:", result)
        return True

    except (requests.RequestException, ValueError) as exc:
        print("Property status sync failed:", str(exc))
        return False

@require_POST
def toggle_availability(request, id):
    property_obj = get_object_or_404(Properties, id=id)

    property_obj.available = not property_obj.available
    property_obj.save(update_fields=["available"])

    if sync_property_status(property_obj):
        messages.success(
            request,
            "Availability updated on the client website."
        )
    else:
        messages.warning(
            request,
            "Sender status updated, but client sync failed. "
            "Check the server console and try again."
        )

    return redirect("submit_properties")


@require_POST
def make_unavailable(request, id):
    property_obj = get_object_or_404(Properties, id=id)

    property_obj.available = False
    property_obj.save(update_fields=["available"])

    if sync_property_status(property_obj):
        messages.success(
            request,
            "Property marked unavailable on the client website."
        )
    else:
        messages.warning(
            request,
            "Property updated locally, but client sync failed."
        )

    return redirect("submit_properties")

@require_POST
def make_available(request, id):
    property_obj = get_object_or_404(Properties, id=id)

    property_obj.available = True
    property_obj.save(update_fields=["available"])

    if sync_property_status(property_obj):
        messages.success(
            request,
            "Property marked available on the client website."
        )
    else:
        messages.warning(
            request,
            "Property updated locally, but client sync failed."
        )

    return redirect("submit_properties")
