from django.db import models
from . import AccessPointModel
from . import FirmwareVersion

class AccessPoint(models.Model):

    # Metadata
    barcodeId = models.CharField(max_length=6, primary_key=True, unique=True)
    model = models.ForeignKey(AccessPointModel, on_delete=models.PROTECT)
    firmware_version = models.ForeignKey(FirmwareVersion,
                                         on_delete=models.PROTECT,
                                         related_name='current_aps',
                                         blank=True, null=True) # Firwmare does not have a firmware_version

    # Network Info
    mac_address = models.CharField(max_length=24, null=True) # Auto-formatting of data
    # These aren't in mongo topologies for Dut. More to come.
    ip_address = models.GenericIPAddressField(blank=True, null=True, default=None)
    bssid_24g = models.CharField(max_length=32, blank=True, verbose_name='2.4G BSSID')
    bssid_5g = models.CharField(max_length=32, blank=True, verbose_name='5G BSSID')
    bssid_6g = models.CharField(max_length=32, blank=True, verbose_name='6G BSSID')
    ssid_24g = models.CharField(max_length=32, blank=True, verbose_name='2.4G SSID')
    ssid_5g = models.CharField(max_length=32, blank=True, verbose_name='5G SSID')
    ssid_6g = models.CharField(max_length=32, blank=True, verbose_name='6G SSID')
    default_24g_channel = models.SmallIntegerField(default=6)
    default_5g_channel = models.SmallIntegerField(default=44)
    default_6g_channel = models.SmallIntegerField(default=65)

    # Misc. Notes
    notes = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.model} {self.barcodeId}'
    # Needed for ETL. Using django models from a standalone python script requires configuration.
    # Enforces either adding this app_label to each model, or adding each model to settings.py INSTALLED_APPS
    class Meta:
        app_label = 'invman'