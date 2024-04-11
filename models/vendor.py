from django.db import models

VENDOR_CHOICES = (
    ('ACTIONTEC',          'Actiontec'),
    ('AIRTIES',            'Airties'),
    ('ARCADYAN',           'Arcadyan'),
    ('ARRIS',              'Arris'),
    ('ASKEY',              'Askey'),
    ('ASUS',               'Asus'),
    ('BROADCOM',           'Broadcom'),
    ('CISCO',              'Cisco'),
    ('COMMSCOPE',          'Commscope'),
    ('D-LINK',             'D-Link'),
    ('EERO',               'Eero'),
    ('GENERAL_POWER_STRIP', 'General Power Strip'),
    ('HITRON',             'Hitron'),
    ('HUMAX',              'Humax'),
    ('INTEL',              'Intel'),
    ('IXIA',               'Ixia'),
    ('JFW',                'Jfw'),
    ('KEYSIGHT',           'Keysight'),
    ('LINKSYS',            'Linksys'),
    ('MARVELL',            'Marvell'),
    ('MOTOROLA',           'Motorola'),
    ('NETGEAR',            'Netgear'),
    ('NOKIA',              'Nokia'),
    ('OCTOSCOPE',          'Octoscope'),
    ('PLUME',              'Plume'),
    ('QUALCOMM',           'Qualcomm'),
    ('QUANTENNA',          'Quantenna'),
    ('RAMSEY',             'Ramsey'),
    ('RUCKUS',             'Ruckus'),
    ('SAGEMCOM',           'Sagemcom'),
    ('SAMSUNG',            'Samsung'),
    ('SERCOMM',            'Sercomm'),
    ('TP-LINK',            'Tp-link'),
    ('TECHNICOLOR',        'Technicolor'),
    ('TEST_VENDOR',        'Test Vendor'),
    ('UBEE',               'Ubee'),
    ('VERIWAVE',           'Veriwave'),
    ('TEST_ENTERPRISE',    'Test_Enterprise')
)

class Vendor(models.Model): 
    company_code = models.CharField(max_length=40, blank=True, unique=True)
    company_name = models.CharField(max_length=40,
                                    default='Vendor Name Here',
                                    primary_key=True, unique=True)
    company_contact_name = models.CharField(max_length=40, blank=True, null=True)
    company_contact_email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'{self.company_name}'
    
    # Needed for ETL. Using django models from a standalone python script requires configuration.
    # Enforces either adding this app_label to each model, or adding each model to settings.py INSTALLED_APPS    
    class Meta:
        app_label = 'invman'