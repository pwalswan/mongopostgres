def get_django_config():
    import sys
    import os
    # Importing models requires Django config
    terra_path = os.path.expanduser('~/projects/terra/django')
    sys.path.append(terra_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

get_django_config()
import django
django.setup()
from invman.models.topology_etl import ETLIxia76Topology, ETLIxia76MultiAPTopology, ETLIxiaWifi6Topology, ETLIxiaWifi6ETopology
from invman.models.firmware_ap import FirmwareVersion
from invman.models.location import Location, LOCATION_TYPE_CHOICES
from invman.models.vendor import Vendor, VENDOR_CHOICES
from invman.models import AccessPoint, AccessPointModel
import utils
import django.db.models as models
from django.db import IntegrityError

class BaseTransformer:
    def __init__(self, mongo_data, collection):
        self.mongo_data = mongo_data
        self.collection = collection

    def transform_collection(self):
        raise NotImplementedError()
    
class LocationTransformer(BaseTransformer):
    '''Copy LOCATION_TYPE_CHOICES in the location model into the location postgres table'''
    def transform_collection(self):
        print(self.collection)
        for location_choice in LOCATION_TYPE_CHOICES:
            Location(name=location_choice[0], location_type=location_choice[1]).save()

class VendorTransformer(BaseTransformer):
    '''Copy VENDOR_CHOICES in the vendor model into the vendor postgres table'''
    def transform_collection(self):
        print(self.collection)
        for vendor_choice in VENDOR_CHOICES:
            Vendor(company_code=vendor_choice[0], company_name=vendor_choice[1]).save()

class AccessPointModelTransformer(BaseTransformer):
    '''Copy all of the inventories.model over into the postgres table. These are like SAC2V1K, R510, etc.
        To be used as a dependency for AccessPoint. Load these before loading AccessPoint.'''
    def transform_collection(self):
        print(self.collection)
        mongo_client = utils.connect_to_mongodb()
        query = {"__t": "Dut"}
        mongo_data = utils.extract_collection(mongo_client, self.collection, query)
        for dut_document in mongo_data:
            print(dut_document['model'])
            dut_row = AccessPointModel()
            dut_mapping = utils.open_file('django/invman/etl/access_point_model.json')

            utils.set_mapped_values(dut_document, dut_row, dut_mapping)

            add_vendor(dut_document, dut_row)

            try:
                dut_row.save()
            except IntegrityError as e:
                print(f"Continuing on IntegrityError: {e}")

class TopologyTransformer(BaseTransformer):
    '''Collection iterator for transformations'''
    def transform_collection(self):
        print('Processing ' + self.collection)

        for document in self.mongo_data:
            # '''Transform a single document'''
            print('Document: ' + document['name'])
            try:
                if document['metaData']['version'] == '7.5':
                    topology_row = ETLIxia76Topology()
                    topology_mapping = utils.open_file('django/invman/etl/ETLIxia76Topology.json')
                elif document['metaData']['version'] == '7.6':
                    topology_row = ETLIxia76Topology()
                    topology_mapping = utils.open_file('django/invman/etl/ETLIxia76Topology.json')
                elif document['metaData']['version'] == '9.x':
                    topology_row = ETLIxiaWifi6ETopology()
                    topology_mapping = utils.open_file('django/invman/etl/ETLIxia76Topology.json')
                else:
                    print('Invalid...')
            except KeyError:
                print('No metadata in mongodb')

            utils.set_mapped_values(document, topology_row, topology_mapping)

            add_location(document, topology_row)

            try:
                topology_row.save()
            except IntegrityError as e:
                print(f"Continuing on IntegrityError: {e}")

class InventoriesTransformer(BaseTransformer):
        def transform_collection(self):
            print('Processing ' + self.collection)
            for document in self.mongo_data:
                if document['__t'] == 'Firmware':
                    try:
                        print('Firmware version ' + str(document['version']))
                        firmware_row = FirmwareVersion()
                        firmware_mapping = utils.open_file('django/invman/etl/firmware_ap.json')
                    except Exception as e:
                        print(f"Continuiung on Exception: {e}")

                    utils.set_mapped_values(document, firmware_row, firmware_mapping)
                    
                    add_access_point_model(document, firmware_row)
                        
                    try:
                        firmware_row.save()
                    except IntegrityError as e:
                        print(f"Continuiung on IntegrityError: {e}")
                    except Exception as e:
                        print(f"Exception: {e}")
                    
                # DUT / Access Point
                elif document['__t'] == 'Dut':
                    try:
                        print('DUT model ' + str(document['model']))
                        dut_row = AccessPoint()
                        dut_mapping = utils.open_file('django/invman/etl/dut.json')
                    except Exception as e:
                        print(f"Continuiung on Exception: {e}")

                    utils.set_mapped_values(document, dut_row, dut_mapping)

                    add_access_point_model(document, dut_row)

                    add_firmware(document, dut_row)

                    try:
                        dut_row.save()
                    except IntegrityError as e:
                        print(f"Continuiung on IntegrityError: {e}")

                else:
                    continue 

def add_vendor(document, row):
    '''Add Vendor model'''
    try:
        theVendor = document['company'].upper()
    except AttributeError:
        print("Continuing on Vendor is None")

    vendor_dict = dict(VENDOR_CHOICES)
    found_vendor = vendor_dict.get(theVendor)
    vendor = Vendor.objects.get(company_name = found_vendor)
    row.vendor = vendor

def add_location(document, row):
    '''Add Location model'''
    try:
        if document['location'].startswith('1'):
            row.location = Location.objects.get(name='lab_1')
        elif document['location'].startswith('2'):
            row.location = Location.objects.get(name='lab_2')
        else:
            row.location = Location.objects.get(name='other')
    except KeyError:
        print('No topology location in mongodb')

def add_access_point_model(document, row):
    try:
        ap_model = AccessPointModel()
        ap_model.model_name = document['model']
        if document['__t'] == 'Firmware':
            row.ap_model = ap_model
        elif document['__t'] == 'Dut':
            row.model = ap_model

    except KeyError:
        print('No model')

def add_firmware(document, row):

    dut_firmware = FirmwareVersion()

    mongo_client_firmware = utils.connect_to_mongodb()
    query = {
        "__t" : "Firmware",
        "_id" : document['firmware']
    }    

    try:
        firmware_version = utils.extract_collection(mongo_client_firmware, 'inventories', query)
        for firmware_document in firmware_version:
            dut_firmware.firmware_name = firmware_document['version']
            row.firmware_version = dut_firmware

    except KeyError:
        print('No model')