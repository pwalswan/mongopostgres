from django.db import models

class Keysight76EthPort(models.Model):
    # Base information
    port_name = models.CharField(max_length=64, unique=True) # 10.3.65.117 Card 3 Port 1
    config_name = models.CharField(max_length=64, primary_key=True,
                                   unique=True) #10.3.65.117_3_1
    # Network information
    switch = models.GenericIPAddressField(blank=True,
                                          null=True)
    switch_port = models.CharField(max_length=10)
    vlan_number = models.SmallIntegerField(default=655)
    # Miscellaneous information
    card_model = models.CharField(choices=(
                                      ('rfx5000', 'RFX 5000'),
                                      ('wbx5000', 'WBX 5000'),
                                      ('other', 'Other')
                                  ),
                                  default='other',
                                  max_length=16,
                                  blank=True)
    
    def __str__(self) -> str:
        return self.port_name
    
    # Needed for ETL. Using django models from a standalone python script requires configuration.
    # Enforces either adding this app_label to each model, or adding each model to settings.py INSTALLED_APPS
    class Meta:
        app_label = 'invman'