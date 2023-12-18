
class SFTRunner:
    def __init__(self,**kwargs):
        self._data_reader = None
    @property
    def data_reader(self):
        print("execute data_reader:" )
        if self._data_reader == None:
            self._data_reader = "hello"
        return self._data_reader


sft = SFTRunner()

dr =  sft.data_reader
print(dr)
