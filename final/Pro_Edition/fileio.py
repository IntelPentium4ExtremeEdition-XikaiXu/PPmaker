import json
import os

class ParameterReader:
    def __init__(self, filename='parameters.json'):
        self.filename = filename

    def load_parameters(self):
        
        if not os.path.exists(self.filename):
            return {"AOO": [], "VOO": [], "AAI": [], "VVI": []} 

        with open(self.filename, 'r') as file:
            data = json.load(file)
        return data

    def get_aoo_parameters(self):
        parameters = self.load_parameters()
        return parameters.get('AOO', [])

    def get_voo_parameters(self):
        parameters = self.load_parameters()
        return parameters.get('VOO', [])

    def get_aii_parameters(self):
        parameters = self.load_parameters()
        return parameters.get('AAI', [])

    def get_vvi_parameters(self):
        parameters = self.load_parameters()
        return parameters.get('VVI', [])

    def get_all_parameters(self):
        parameters = self.load_parameters()
        return parameters

if __name__ == "__main__":
    reader = ParameterReader()
    aoo_params = reader.get_aoo_parameters()
    voo_params = reader.get_voo_parameters()
    aai_params = reader.get_aii_parameters()
    vvi_params = reader.get_vvi_parameters()
    all_params = reader.get_all_parameters()

