
import requests
from django.conf import settings


def sync_property(prop):
    base_url = settings.REAL_ESTATE_RECEIVER_URL.rstrip("/")
    endpoint = f"{base_url}/api/receive-property/"

    data = {
        "source_property_id": str(prop.pk),
        "furnished": prop.furnished or "",
        "location": prop.location or "",
        "price": str(prop.price),
        "bhk": str(prop.bhk),
        "contact": prop.contact or "",
        "published": str(prop.published).lower(),
        "available": str(prop.available).lower(),
    }

    opened_files = []
    files = {}

    try:
        # Transfer both main images, if present.
        for field_name in ("house_image", "hall_image"):
            field_file = getattr(prop, field_name)
            if field_file:
                field_file.open("rb")
                opened_files.append(field_file)
                files[field_name] = (
                    field_file.name.split("/")[-1],
                    field_file.file,
                )

        # Transfer every gallery image.
        for index, gallery_image in enumerate(
            prop.images.all().order_by("pk")
        ):
            gallery_image.image.open("rb")
            opened_files.append(gallery_image.image)

            files[f"gallery_{index}"] = (
                gallery_image.image.name.split("/")[-1],
                gallery_image.image.file,
            )
            data[f"gallery_type_{index}"] = (
                gallery_image.image_type or "gallery"
            )

        response = requests.post(
            endpoint,
            data=data,
            files=files,
            headers={
                "Authorization": (
                    f"Bearer {settings.RECEIVE_PROPERTY_API_TOKEN}"
                )
            },
            timeout=60,
        )

        response.raise_for_status()
        return response.json()

    finally:
        for field_file in opened_files:
            field_file.close()
