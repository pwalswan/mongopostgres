from django.db import models


LOCATION_TYPE_CHOICES = (
    ('lab_1', 'Lab 1'),
    ('lab_2', 'Lab 2'),
    ('lab_3', 'Lab 3'),
    ('lab_4', 'Lab 4'),
    ('eng_desk', 'Engineer Desk'),
    ('other', 'Other')
)

class Location(models.Model):
    name = models.CharField(max_length=50, primary_key=True, unique=True)
    location_type = models.CharField(
        choices=LOCATION_TYPE_CHOICES,
        default='other',
        max_length=20
    )
    address = models.CharField(max_length=128, blank=True)

    def __str__(self) -> str:
        return self.name 

    # Needed for ETL. Using django models from a standalone python script requires configuration.
    # Enforces either adding this app_label to each model, or adding each model to settings.py INSTALLED_APPS
    class Meta:
        app_label = 'invman'