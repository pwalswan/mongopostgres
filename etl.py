import utils
from transformers import LocationTransformer, VendorTransformer, AccessPointModelTransformer, TopologyTransformer, InventoriesTransformer

def main():
    '''Entrypoint'''
    print('\nStarting pipeline...')

    config = utils.get_config()

    mongo_client = utils.connect_to_mongodb()

    collection_names = config['collection_names']

    for collection_name, process in collection_names.items():

        if process:
            mongo_data = utils.extract_collection(mongo_client, collection_name, '')
            
            if collection_name == 'location':
                transformer = LocationTransformer(mongo_data, 'location')
                transformer.transform_collection()
                print('*** Completed location import ***')
            elif collection_name == 'vendor':
                transformer = VendorTransformer(mongo_data, 'vendor')
                transformer.transform_collection()
                print('*** Completed vendor import ***')
            if collection_name == 'topology':
                transformer = TopologyTransformer(mongo_data, 'topology')
                transformer.transform_collection()
                print('Data inserted into ETL tables in postgres. Do an INSERT INTO SELECT to move them to the TERRA tables.')
            if collection_name == 'inventories':
                if config['load_access_point_device_model']:
                    transformer = AccessPointModelTransformer(mongo_data, 'inventories')
                    transformer.transform_collection()
                    print('*** Completed AccessPointModelTransformer import ***')
                transformer = InventoriesTransformer(mongo_data, 'inventories')
                transformer.transform_collection()
                print('*** Completed Inventories import ***')

    print('\nPipeline complete!\n')

if __name__ == '__main__':
    main()