
# I did not create these models! This mongopostgres repo is the python code up one directory from the models directory.
# Topologies should have one model, not one model for each Topology. I did not create these models.

# This is a duplicate of topology.py model, so I didn't overwrite their manual model entris in postgres.

from django.db import models
from . import AccessPoint
from . import Keysight76EthPort
from . import Location

ATTENUATOR_PORT_CHOICES = (
    ('1,2,3,4', '1-4'),
    ('5,6,7,8', '5-8'),
    ('9,10,11,12', '9-12'),
    ('13,14,15,16', '13-16')
)

# Base topology model 
class ETLBaseTopology(models.Model): 

    id = models.BigAutoField(primary_key=True)
    # id_mongo = models.UUIDField(unique=True)

    # General Information
    name = models.CharField(max_length=64,
                            unique=True)

    # Status/AP Information
    is_active = models.BooleanField(default=False)
    active_dut = models.BooleanField(default=False)
    current_dut = models.OneToOneField(
        AccessPoint,
        on_delete=models.PROTECT,
        blank=True, null=True)

    # Base testing capabilities (expected for all topologies)
    support_11ag = models.BooleanField(default=True)
    support_11n = models.BooleanField(default=True)
    support_11ac = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
        # Needed for ETL. Using django models from a standalone python script requires configuration.
        # Enforces either adding this app_label to each model, or adding each model to settings.py INSTALLED_APPS
        app_label = 'invman'


class ETLIxia76Topology(ETLBaseTopology):
    # General Info
    location = models.ForeignKey(Location, on_delete=models.PROTECT,
                                 related_name='ixia76_location_etl')

    # AX/6G Testing Capabilities
    support_11ax = models.BooleanField(default=False)
    support_6e = models.BooleanField(default=False)
    support_7 = models.BooleanField(default=False)

    # Server Info
    ixia_web_server = models.GenericIPAddressField(default="10.92.112.0")
    license_server = models.GenericIPAddressField(default='10.3.65.113')

    # Attenuator Information (separated to handle multiple JFW used)
    jfw_atten_24 = models.GenericIPAddressField(default='10.3.65.0')
    jfw_atten_24_ports = models.CharField(
        max_length=11,
        choices= ATTENUATOR_PORT_CHOICES
    )
    jfw_atten_5 = models.GenericIPAddressField(blank=True, null=True)
    jfw_atten_5_ports = models.CharField(
        max_length=11,
        choices= ATTENUATOR_PORT_CHOICES
    )

    # Ixia Chassis/Card/Port information
    ixia_wifi_port_24g = models.CharField(max_length=64) # 10.3.65.114_6_1
    ixia_wifi_port_5g = models.CharField(max_length=64)
    ixia_wan_port_active = models.BooleanField(default=False)
    ixia_wan_eth_port = models.OneToOneField(
        Keysight76EthPort,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='wanport_etl'
    )
    ixia_lan1_port_active = models.BooleanField(default=False)
    ixia_lan1_eth_port = models.OneToOneField(
        Keysight76EthPort,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='lan1port_etl'
    )
    ixia_lan2_port_active = models.BooleanField(default=False)
    ixia_lan2_eth_port = models.OneToOneField(
        Keysight76EthPort,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='lan2port_etl'
    )

    # Switch information
    switch_ip_address = models.GenericIPAddressField(blank=True, null=True)
    wan_switch_port = models.CharField(max_length=10)
    wan_vlan_num = models.SmallIntegerField(default=655)
    lan1_switch_port = models.CharField(max_length=10)
    lan1_vlan_num = models.SmallIntegerField(blank=True, null=True)
    lan2_switch_port = models.CharField(max_length=10)
    lan2_vlan_num = models.SmallIntegerField(blank=True, null=True)

    # DUT Controller information
    rpi_dut_controller = models.GenericIPAddressField(blank=True, null=True)
    rpi_config_switch_port = models.CharField(max_length=10, default="Te1/0/21",
                                              blank=True, null=True)

class ETLIxia76MultiAPTopology(ETLBaseTopology):
    # General Info
    location = models.ForeignKey(Location, on_delete=models.PROTECT,
                                 related_name='ixia76_multiap_location_etl')
    
    # AX/6G Testing Capabilities
    support_11ax = models.BooleanField(default=False)
    support_6e = models.BooleanField(default=False)
    support_7 = models.BooleanField(default=False)

    # Server Info
    ixia_web_server = models.GenericIPAddressField(default="10.92.112.0")
    license_server = models.GenericIPAddressField(default='10.3.65.113')

    # Second AP/Extender information
    second_chamber_name = models.CharField(max_length=64)
    second_dut_active = models.BooleanField(default=True)
    dut2 = models.OneToOneField(
        AccessPoint,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='extender_ap_etl')

    # Attenuator Information (separated to handle multiple JFW used)
    jfw_atten = models.GenericIPAddressField(default='10.3.65.0')
    jfw_atten_24_ports = models.CharField(
        max_length=11,
        choices= ATTENUATOR_PORT_CHOICES
    )
    jfw_atten_5_ports = models.CharField(
        max_length=11,
        choices= ATTENUATOR_PORT_CHOICES
    )

    # (Primary DUT) Ixia Ethernet cards/ports information
    dut1_ixia_wan_port_active = models.BooleanField(default=False)
    dut1_ixia_wan_eth_port = models.OneToOneField(
        Keysight76EthPort,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='dut1_wanport_etl'
    )
    dut1_ixia_lan1_port_active = models.BooleanField(default=False)
    dut1_ixia_lan1_eth_port = models.OneToOneField(
        Keysight76EthPort,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='dut1_lan1port_etl'
    )
    dut1_ixia_lan2_port_active = models.BooleanField(default=False)
    dut1_ixia_lan2_eth_port = models.OneToOneField(
        Keysight76EthPort,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='dut1_lan2port_etl'
    )

    # (Secondary/Extender DUT) Ixia Ethernet cards/ports information
    dut2_ixia_lan1_port_active = models.BooleanField(default=False)
    dut2_ixia_lan1_eth_port = models.OneToOneField(
        Keysight76EthPort,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='dut2_lan1port_etl'
    )
    dut2_ixia_lan2_port_active = models.BooleanField(default=False)
    dut2_ixia_lan2_eth_port = models.OneToOneField(
        Keysight76EthPort,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='dut2_lan2port_etl'
    )

    # (Primary DUT) Switch information
    dut1_switch_ip_address = models.GenericIPAddressField(blank=True, null=True)
    dut1_wan_switch_port = models.CharField(max_length=10)
    dut1_wan_vlan_num = models.SmallIntegerField(default=655)
    dut1_lan1_switch_port = models.CharField(max_length=10)
    dut1_lan1_vlan_num = models.SmallIntegerField(blank=True, null=True)
    dut1_lan2_switch_port = models.CharField(max_length=10)
    dut1_lan2_vlan_num = models.SmallIntegerField(blank=True, null=True)

    # (Secondary/Extender DUT) Switch information
    dut2_switch_ip_address = models.GenericIPAddressField(blank=True, null=True)
    dut2_lan1_switch_port = models.CharField(max_length=10)
    dut2_lan1_vlan_num = models.SmallIntegerField(blank=True, null=True)
    dut2_lan2_switch_port = models.CharField(max_length=10)
    dut2_lan2_vlan_num = models.SmallIntegerField(blank=True, null=True)

    # DUT Controller information
    rpi_dut_controller = models.GenericIPAddressField(blank=True, null=True)
    rpi_config_switch_port = models.CharField(max_length=10, default="Te1/0/21",
                                              blank=True, null=True)

class ETLIxiaWifi6Topology(ETLBaseTopology):
    # General Info
    location = models.ForeignKey(Location, on_delete=models.PROTECT,
                                 related_name='ixia_wifi6_location_etl')

    # AX/6G Testing Capabilities
    support_11ax = models.BooleanField(default=True)
    support_6e = models.BooleanField(default=False)
    support_7 = models.BooleanField(default=False)

    # Web Server Info
    ixia_web_server = models.GenericIPAddressField(default="10.92.112.0")
    license_server = models.GenericIPAddressField(default='10.3.65.104')

    # Attenuator Information (separated to handle multiple JFW used)
    jfw_atten = models.GenericIPAddressField(default='0.0.0.0')
    jfw_atten_24_ports = models.CharField(
        max_length=11,
        choices= ATTENUATOR_PORT_CHOICES
    )
    jfw_atten_5_ports = models.CharField(
        max_length=11,
        choices= ATTENUATOR_PORT_CHOICES
    )

    # Ixia Chassis/Card/Port information
    ixia_wifi_port_24g = models.CharField(max_length=64)
    ixia_wifi_port_5g = models.CharField(max_length=64)
    ixia_wan_eth_port = models.CharField(max_length=64)
    ixia_lan1_eth_port = models.CharField(max_length=64)
    ixia_lan2_eth_port = models.CharField(max_length=64)

    # Switch information
    switch_ip_address = models.GenericIPAddressField(blank=True, null=True)
    wan_switch_port = models.CharField(max_length=10)
    wan_vlan_num = models.SmallIntegerField(default=655)
    lan1_switch_port = models.CharField(max_length=10)
    lan1_vlan_num = models.SmallIntegerField(blank=True, null=True)
    lan2_switch_port = models.CharField(max_length=10)
    lan2_vlan_num = models.SmallIntegerField(blank=True, null=True)

    # DUT Controller information
    rpi_dut_controller = models.GenericIPAddressField(blank=True, null=True)
    rpi_config_switch_port = models.CharField(max_length=10, default="Te1/0/21",
                                              blank=True, null=True)
        
class ETLIxiaWifi6ETopology(ETLBaseTopology):
    # General Info
    location = models.ForeignKey(Location, on_delete=models.PROTECT,
                                 related_name='ixia_wifi6e_location_etl')

    # AX/6G Testing Capabilities
    support_11ax = models.BooleanField(default=True)
    support_6e = models.BooleanField(default=True)
    support_7 = models.BooleanField(default=False)

    # Web Server Info
    ixia_web_server = models.GenericIPAddressField(default="10.92.112.0")
    license_server = models.GenericIPAddressField(default='10.3.65.104')
    
    # Attenuator Information (separated to handle multiple JFW used)
    jfw_atten = models.GenericIPAddressField(default='10.92.114.0')
    # jfw_atten_24_ports = models.CharField(
    #     max_length=11,
    #     choices= ATTENUATOR_PORT_CHOICES,
    #     default=ATTENUATOR_PORT_CHOICES[1]
    # )
    # jfw_atten_5_ports = models.CharField(
    #     max_length=11,
    #     choices= ATTENUATOR_PORT_CHOICES,
    #     default=ATTENUATOR_PORT_CHOICES[0]
    # )
    # jfw_atten_6_ports = models.CharField(
    #     max_length=11,
    #     choices= ATTENUATOR_PORT_CHOICES,
    #     default=ATTENUATOR_PORT_CHOICES[2]
    # )


    # Ixia Chassis/Card/Port information
    ixia_wifi_port_24g = models.CharField(max_length=64)
    ixia_wifi_port_5g = models.CharField(max_length=64)
    ixia_wifi_port_6g = models.CharField(max_length=64)
    ixia_wan_eth_port = models.CharField(max_length=64)
    ixia_lan1_eth_port = models.CharField(max_length=64)
    ixia_lan2_eth_port = models.CharField(max_length=64)

    # Switch information
    switch_ip_address = models.GenericIPAddressField(default="10.92.114.13")
    wan_switch_port = models.CharField(max_length=10)
    wan_vlan_num = models.SmallIntegerField(default=655)
    lan1_switch_port = models.CharField(max_length=10)
    lan1_vlan_num = models.SmallIntegerField(blank=True, null=True)
    lan2_switch_port = models.CharField(max_length=10)
    lan2_vlan_num = models.SmallIntegerField(blank=True, null=True)

    # DUT Controller information
    rpi_dut_controller = models.GenericIPAddressField(blank=True, null=True)
    rpi_config_switch_port = models.CharField(max_length=10, default="Te1/0/21",
                                              blank=True, null=True)

