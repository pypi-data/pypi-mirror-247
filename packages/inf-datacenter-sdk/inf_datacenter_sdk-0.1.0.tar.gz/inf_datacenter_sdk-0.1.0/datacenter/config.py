
from .io_util import load_yaml_file,check_file_exists

DEFAULT_ENDPOINT = 'http://localhost:8002'
DEFAULT_TOKEN = '123456'
DEFAULT_MNT_DIR = '/mnt/mlops/dataset/'
class Config:
    def __init__(self, config_file_path = None):
        if config_file_path != None and len(config_file_path)>0:
            self.config = self.load_config(config_file_path)
       
    def load_config(self, config_file_path):

        return load_yaml_file(config_file_path)


    def get_end_point(self):
        if self.endpoint!=None:
            return self.endpoint
        if self.config!=None:
            return self.config['datacenter']['endpoint']
        else:
            return DEFAULT_ENDPOINT
    def get_token(self):
        if self.config!=None:
            return self.config['datacenter']['token']
        else:
            return DEFAULT_TOKEN

    def get_mnt_dir(self):
        if self.config!=None:
            return self.config['mnt_dir']
        else:
            return DEFAULT_MNT_DIR
    
default_config = None
# if check_file_exists('datacenter-config.yaml'):
#     default_config = Config('datacenter-config.yaml')    
