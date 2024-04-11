from django.db import models
from . import Vendor

BAND_5G_CHOICES = (
    (40, '40'),
    (80, '80'),
    (160, '160')
)   

BAND_2G_CHOICES = (
    (20, '20'),
    (40, '40'),
    (80, '80')
)   

class AccessPointModel(models.Model):
    model_name = models.CharField(max_length=32, primary_key=True, unique=True)
    
    # Metadata
    engineer_build = models.BooleanField(default=False) # model is pre-production for engineering testing 
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    use_type = models.CharField(choices=(
                                    ('residential', 'Residential'),
                                    ('smb', 'SMB'),
                                    ('enterprise', 'Enterprise'),
                                    ('other', 'Other (N/A)')
                                ),
                                null=True,
                                default='residential',
                                max_length=16)
    chipset = models.CharField(max_length=10, null=True, choices=(
                                   ('qualcomm', 'Qualcomm'),
                                   ('broadcomm', 'Broadcomm')))

    # Capabilities
    scp = models.BooleanField(default=True, null=True)
    ipv4 = models.BooleanField(default=True, null=True)
    ipv6 = models.BooleanField(default=False, null=True)
    support_11ag = models.BooleanField(default=True, null=True)
    support_11n = models.BooleanField(default=True, null=True)
    support_11ac = models.BooleanField(default=True, null=True)
    support_11ax = models.BooleanField(default=False, null=True)
    support_6e = models.BooleanField(default=False, null=True)
    support_7 = models.BooleanField(default=False, null=True)

    max_band_2g = models.PositiveSmallIntegerField(
        choices = BAND_2G_CHOICES,
        default = 40,
        null=True
    )
    max_band_5g = models.PositiveSmallIntegerField(
        choices = BAND_5G_CHOICES,
        default = 80,
        null=True
    )

    def __str__(self) -> str:
        return self.model_name

    # Needed for ETL. Using django models from a standalone python script requires configuration.
    # Enforces either adding this app_label to each model, or adding each model to settings.py INSTALLED_APPS
    class Meta:
        app_label = 'invman'