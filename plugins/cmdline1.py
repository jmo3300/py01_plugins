import argparse
from plugins.ui_base import UIBase

class UI(UIBase):
    
    def execute(self):
    
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', '--a_option', help='considers option a', action='store_true')
        parser.add_argument('-b', '--b_option', help='considers option b', action='store_true')
        return parser.parse_args()
