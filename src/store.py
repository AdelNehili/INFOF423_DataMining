from glob import glob
from os.path import join, dirname, basename
from utils import load_df, filter_df

class DataStore:
    
    def __init__(self, load_files=glob(join(dirname(dirname(__file__)), "data", "ar41_for_ulb_mini.csv"))):
        self.cache = {}

        if load_files:
            for file in load_files:
                self.cache[file] = load_df(file)
    
    def filter(self, file, filters):
        if file not in self.cache:
            self.cache[file] = load_df(file)
        return filter_df(self.cache[file], filters)
    
    def get_df(self, name):
        if name not in self.cache:
            return
        return self.cache[name]

