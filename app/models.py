from django.db import models


class Properties(models.Model):

    furnished = models.CharField(max_length=100)

    location = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    bhk = models.IntegerField()

    contact = models.CharField(max_length=15)

    house_image = models.ImageField(
        upload_to="properties/",
        blank=True,
        null=True
    )

    hall_image = models.ImageField(
        upload_to="properties/",
        blank=True,
        null=True
    )

    published = models.BooleanField(
        default=False
    )

    available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.furnished


class PropertyImage(models.Model):

    property = models.ForeignKey(
        Properties,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="properties/"
    )

    image_type = models.CharField(
        max_length=20
    )

    def __str__(self):
        return f"{self.property.furnished} - {self.image_type}"