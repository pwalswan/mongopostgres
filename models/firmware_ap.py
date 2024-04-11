from django.db import models
from . import AccessPointModel

class FirmwareVersion(models.Model): #WIP - Make name AP specific?? 
    firmware_name = models.CharField(max_length=128, primary_key=True,
                                     unique=True) # Need AP Model in Name for uniqueness
    ap_model = models.ForeignKey(AccessPointModel,
                                 on_delete=models.PROTECT)
    certified = models.BooleanField(default=False, null=True)
    in_field = models.BooleanField(default=False, null=True)

    def __str__(self) -> str:
        return f'{self.firmware_name}'

    # Needed for ETL. Using django models from a standalone python script requires configuration.
    # Enforces either adding this app_label to each model, or adding each model to settings.py INSTALLED_APPS
    class Meta:
        app_label = 'invman'