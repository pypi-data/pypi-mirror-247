
class DataStoreCluster():

    def __init__(self, spartacloud_api_instance, target_node:int=None):
        self.spartacloud_api_instance = spartacloud_api_instance
        self.target_node = target_node
        
    def status(self) -> dict:
        '''
        Get redis data store cluster status
        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        return self.spartacloud_api_instance.query_service('get_data_store_cluster_status', data_dict)

    def keys(self) -> dict:
        '''
        Get redis data store cluster keys
        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        return self.spartacloud_api_instance.query_service('get_data_store_cluster_keys', data_dict)

    # *****************************************************************************
    # OPERATION ENDPOINT
    # *****************************************************************************
    def get(self, key) -> dict:
        '''
        Get redis data store cluster get value (can receive multiple value from different nodes)
        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['operation'] = 'get'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)
    
    def set(self, key, value) -> dict:
        '''
        Put data to redis (if target_node not defined, put to all nodes)
        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['value'] = value
        data_dict['operation'] = 'set'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)
    
    def delete(self, *keys) -> dict:
        '''
        Delete data to redis
        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['keys'] = keys
        data_dict['operation'] = 'delete'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)
    
    def rpush(self, key, *values) -> dict:
        '''

        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['values'] = values
        data_dict['operation'] = 'rpush'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)
    
    def lrange(self, key, start, end) -> dict:
        '''
        
        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['start'] = start
        data_dict['end'] = end
        data_dict['operation'] = 'lrange'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)
    
    def hset(self, key, field, value) -> dict:
        '''
        
        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['field'] = field
        data_dict['value'] = value
        data_dict['operation'] = 'hset'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)
    
    def hget(self, key, field) -> dict:
        '''
        
        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['field'] = field
        data_dict['operation'] = 'hget'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)
    
    def sadd(self, key, *members) -> dict:
        '''
       
        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['members'] = members
        data_dict['operation'] = 'sadd'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)

    def smembers(self, key) -> dict:
        '''

        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['operation'] = 'smembers'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)

    def zadd(self, key, mapping) -> dict:
        '''

        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['mapping'] = mapping
        data_dict['operation'] = 'zadd'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)

    def zrangebyscore(self, key, min, max) -> dict:
        '''
 
        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['min'] = min
        data_dict['max'] = max
        data_dict['operation'] = 'zrangebyscore'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)

    def expire(self, key, seconds) -> dict:
        '''

        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['seconds'] = seconds
        data_dict['operation'] = 'expire'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)

    def ttl(self, key) -> dict:
        '''

        '''
        data_dict = self.spartacloud_api_instance.get_common_api_params()
        data_dict['target_node'] = self.target_node
        data_dict['key'] = key
        data_dict['operation'] = 'ttl'
        return self.spartacloud_api_instance.query_service('operation_data_store_cluster', data_dict)
