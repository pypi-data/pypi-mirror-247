import os
from spartacloud_api_utils import get_ws_settings, request_service
from datastore_api import DataStore as DataStore
from datastore_api_cluster import DataStoreCluster as DataStoreCluster

class Spartacloud:

    def __init__(self, api_key=None):
        self._set_api_key(api_key) # This key can be found on the network panel of Spartacloud GUI 

    def _set_api_key(self, api_key=None):
        '''
        Set api key
        '''
        api_key_env = os.getenv('SPARTACLOUD_API_KEY', None)
        if api_key_env is not None:
            self.api_key = api_key_env
            self._prepare_ws_settings()
            return
        
        if api_key is not None:
            self.api_key = api_key
            self._prepare_ws_settings()
            return
        
    def _prepare_ws_settings(self):
        '''
        Prepare web services settings
        '''
        if hasattr(self, 'api_key'):
            self.domain_or_ip, self.http_port, self.api_token_id, _, _ = get_ws_settings(self.api_key)
        
    def override_settings(self, domain_or_ip=None, http_port=None, api_token_id=None):
        '''
        Override api settings
        '''
        if domain_or_ip is None or http_port is None or api_token_id is None:
            raise Exception('Invalid parameters. domain_or_ip, http_port and api_token_id parameters must be valid')
        self.domain_or_ip = domain_or_ip
        self.http_port = http_port
        self.api_token_id = api_token_id

    def get_common_api_params(self) -> dict:
        return {
            'api_token_id': self.api_token_id,
        }
    
    def get_computer_nodes(self):
        '''
        Get list of cluster nodes
        '''
        data_dict = self.get_common_api_params()
        return self.query_service('get_computer_nodes', data_dict)

    def get_metrics_cluster(self):
        '''
        Get cluster metrics of the cluster (all nodes)
        '''
        data_dict = self.get_common_api_params()
        return self.query_service('get_metrics_cluster', data_dict)
    
    def get_status_cluster(self):
        '''
        Get status of the cluster (all nodes)
        '''
        data_dict = self.get_common_api_params()
        return self.query_service('get_status_cluster', data_dict)

    def get_cpu_cluster(self):
        '''
        Get cluster cpu metrics of the cluster (all nodes)
        '''
        data_dict = self.get_common_api_params()
        return self.query_service('get_cpu_cluster', data_dict)

    def get_mem_cluster(self):
        '''
        Get cluster cpu ram of the cluster (all nodes)
        '''
        data_dict = self.get_common_api_params()
        return self.query_service('get_mem_cluster', data_dict)
    
    def get_disk_cluster(self, path_disk='/host'):
        '''
        Get cluster disk of the cluster (all nodes)
        '''
        data_dict = self.get_common_api_params()
        data_dict['path_disk'] = path_disk
        return self.query_service('get_disk_cluster', data_dict)
    
    def distribute_job(self, job_cmd, job_name=None, target_node=None, target_cpu=None, target_mem=None, store_stdout=True, b_rerun=False):
        '''
        Distribute jobs to the spartacloud cluster (cluster entrypoint is worker node)
        '''
        if job_cmd is None:
            raise Exception('You must add a command. It can be a python script, a docker exec command, a shell command etc...')

        data_dict = self.get_common_api_params()
        data_dict['job_cmd'] = job_cmd
        data_dict['job_name'] = job_name
        data_dict['target_node'] = target_node
        data_dict['target_cpu'] = target_cpu
        data_dict['target_mem'] = target_mem
        data_dict['store_stdout'] = store_stdout
        data_dict['b_rerun'] = b_rerun
        return self.query_service('distribute_job', data_dict)
    
    def get_jobs(self):
        '''
        Get list of my jobs
        '''
        data_dict = self.get_common_api_params()
        return self.query_service('get_jobs', data_dict)

    def get_jobs_status(self):
        '''
        Get status of all jobs
        '''
        data_dict = self.get_common_api_params()
        return self.query_service('get_jobs_status', data_dict)
    
    def cancel_job(self, uuid):
        '''
        Cancel a specific job
        '''
        data_dict = self.get_common_api_params()
        if uuid is not None:
            data_dict['uuid'] = uuid
            return self.query_service('cancel_job', data_dict)
        
        err_msg = 'uuid is None. You must specify the uuid as input'
        print(err_msg)
        return {
            'res': -1,
            'errorMsg': err_msg
        }
    
    def cancel_all_jobs(self):
        '''
        Cancel all jobs
        '''
        data_dict = self.get_common_api_params()
        return self.query_service('cancel_all_jobs', data_dict)
    
    def get_job_std(self, uuid):
        '''
        Get job stdout and stderr
        '''
        data_dict = self.get_common_api_params()
        if uuid is not None:
            data_dict['uuid'] = uuid
            return self.query_service('get_job_std', data_dict)

        err_msg = 'uuid is None. You must specify the uuid as input'
        print(err_msg)
        return {
            'res': -1,
            'errorMsg': err_msg
        }

    def delete_job(self, uuid):
        '''
        Delete a job
        '''
        data_dict = self.get_common_api_params()
        if uuid is not None:
            data_dict['uuid'] = uuid
            return self.query_service('delete_job', data_dict)

        err_msg = 'uuid is None. You must specify the uuid as input'
        print(err_msg)
        return {
            'res': -1,
            'errorMsg': err_msg
        }
    
    def put_resource(self, path_to_upload, path_destination):
        '''
        TODO SPARTACLOUD: To implement
        path_destination: relative to /spartacloud_shared/ directory 
        '''
        pass
    
    def get_resource(self, resource_path):        
        '''
        TODO SPARTACLOUD: To implement
        resource_path: relative to /spartacloud_shared/ directory 
        '''
        pass

    def get_data_store(self, host=None, port=None, password=None, db=0) -> DataStore:
        '''
        Get redis data store object
        '''
        if host is None:
            _, _, _, port, password = get_ws_settings(self.api_key)

        data_store = DataStore(host, port, password, db=db)
        return data_store
    
    def get_data_store_cluster(self, target_node:int=None):
        '''
        
        '''
        return DataStoreCluster(spartacloud_api_instance=self, target_node=target_node)
        
    def query_service(self, service_name:str, data_dict:dict) -> dict:
        '''
        POST requests
        '''
        return request_service(self, service_name=service_name, data_dict=data_dict)
    
    def help(self) -> list:
        '''
        
        '''
        methods = [method for method in dir(self) if callable(getattr(self, method))]
        return methods