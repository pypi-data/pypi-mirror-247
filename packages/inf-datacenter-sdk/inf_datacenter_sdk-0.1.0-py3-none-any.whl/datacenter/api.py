from .config import Config
from .io_util import read_jsonl_to_list
import requests


class DatasetSDK:
    def __init__(self,config_path=None,endpoint=None,token=None,mntDir = None):
        
        self.config = Config(config_file_path=config_path)
        if  (endpoint!=None):
            self.endpoint = endpoint
        else:
            self.endpoint =  self.config .get_end_point()
        if (token!=None):
            self.token = token
        else:
            self.token = self.config.get_token()
        if(mntDir!=None):
            self.mntDir = mntDir
        else:

            self.mntDir = self.config.get_mnt_dir()


    def get_data_path(self,datasetId):
        uri= '/api/v1/dataset/getDatasetModeById'
        url = self.endpoint+uri
        payload = {
            'id':datasetId,
            'token':self.token
            }

        response = requests.post(url=url,json=payload)
        if response.status_code == 200:
            json_data = response.json()

            dispatch_status =  json_data['data']['dispatch_status']
            if dispatch_status != 3:
                print("Error: dataset not dispatched yet, status_code : "+ dispatch_status)
                return None
            
            dispatch_path = json_data['data']['dispatch_store_path']
            if len(dispatch_path) == 0 :
                print("Error: fail to find the data path")
                return None
            return dispatch_path    
            
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.text}")

    def get_full_data(self,datasetId):

        path =  self.get_data_path(datasetId)
        print('dataset name :'+path)
        if(path==None):
            return None
        if(self.mntDir!=None):
            path = self.mntDir+path
        data_json_list  =read_jsonl_to_list(path)
        print("get_full_data size: "+ len(data_json_list))        
        return data_json_list