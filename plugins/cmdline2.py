import argparse
from plugins.ui_base import UIBase

class UI(UIBase):
    
    def execute(self):
    
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--c_option', help='considers option c', action='store_true')
        parser.add_argument('-d', '--d_option', help='considers option d', action='store_true')
        return parser.parse_args()
