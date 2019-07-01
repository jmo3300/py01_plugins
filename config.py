# coding:utf-8

import os
import logging
from configparser import ConfigParser

class Config:

    GENERAL = 'general'
    
    PATHS = 'paths'
    
    UI = 'ui'

    GUI_TK = 'gui_tk'
    GUI_WX = 'gui_wx'
    
    DIR_PLUGINS = 'dir.plugins'
    DIR_PLUGINS_DEFAULTNAME = 'plugins'
    DIR_LOGS = 'dir.logs'
    DIR_LOGS_DEFAULTNAME = 'logs'

    _app = None
    _config_filename = None
    _log = None

    cfg = ConfigParser(interpolation=None)

    def __init__(self, app):
        
        self._app = app

        self._config_filename = self.get_app() + '.cfg'

        try:
            with open(self._config_filename):
                self.cfg.read(self._config_filename)
        except IOError:
            self._create_config()

        self.check_paths()

        self._init_log()
    
    def _create_config(self):

        root_directory = os.getcwd()
        plugins_directory = os.path.join(root_directory, Config.DIR_PLUGINS_DEFAULTNAME)
        logs_directory = os.path.join(root_directory, Config.DIR_LOGS_DEFAULTNAME)

        self.cfg[Config.GENERAL] = {
            Config.UI: Config.GUI_WX,
            }

        self.cfg[Config.PATHS] = {
            Config.DIR_PLUGINS: plugins_directory,
            Config.DIR_LOGS: logs_directory,
            }
        
        with open(self.get_config_filename(), 'w') as config_file:
            self.cfg.write(config_file)
        
    def _init_log(self):
        
        # TODO: separate log file per run
        # LOG
        self._log = logging.getLogger(self.get_app())
        self._log.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(logging.DEBUG)
        self._log.addHandler(sh)
        
        file_name = os.path.join(self.cfg[Config.PATHS][Config.DIR_LOGS], self.get_app() + '.log')
        fh = logging.FileHandler(file_name, mode='a')
        fh.setFormatter(fmt)
        fh.setLevel(logging.DEBUG)
        self._log.addHandler(fh)

    def get_app(self):
        return self._app
    
    def get_log(self):
        return self._log
    
    def get_config_filename(self):
        return self._config_filename
    
    def get_config_parser(self):
        return self.cfg

    def check_paths(self):

        self.check_path(self.cfg[Config.PATHS][Config.DIR_PLUGINS])
        self.check_path(self.cfg[Config.PATHS][Config.DIR_LOGS])

    def check_path(self, directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass
