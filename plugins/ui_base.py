import argparse

class UIBase():
    
    _config = None

    def __init__(self, config):
        self._config = config
    
    def get_config(self):
        return self._config
    
    def execute(self):
    
        parser = argparse.ArgumentParser()
#         parser.add_argument('-c', '--c_option', help='considers option c', action='store_true')
#         parser.add_argument('-d', '--d_option', help='considers option d', action='store_true')
        return parser.parse_args()
        