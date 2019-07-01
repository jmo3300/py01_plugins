import os
import sys
import importlib
from config import Config


_app = os.path.splitext(os.path.basename(__file__))[0]

# create configuration
# main part of configuration is getting parameter values 
# this will be done using configparser
# additionally Config does e.a. log system initialization, 
# provides all constants for fetching the parameters and some other 
config = Config(_app)
cfg = config.get_config_parser()

def main():

#     sys.argv.append('-a')       # option a is available only in cmdline1
#     sys.argv.append('-c')       # option c is available only in cmdline2
#     sys.argv.append('-e')       # option e is available only in gui
    sys.argv.append('-f')       # option f is available only in gui
#     sys.argv.append('-h')     # simulates -h / --help pragram argument
    
    # fetch module_name from config file
    ui_module_name = os.path.basename(cfg[Config.PATHS][Config.DIR_PLUGINS]) + '.' + cfg[Config.GENERAL][Config.UI]
    print('ui module: ' + ui_module_name)
    
    args = None
    try:
        ui_module = importlib.import_module(ui_module_name, '.')
        ui = ui_module.UI(config)
        args = ui.execute()         # commend line ui validates the 
    except ModuleNotFoundError:
        print('no module for ui {} not found'.format(ui_module_name))
    except SystemExit:
        print('ui {} found invalid program arguments'.format(ui_module_name))
        sys.exit(2)
#     except:
#         print("Unexpected error:", sys.exc_info()[0])
    try:
        print('a_option: ' + str(args.a_option))
    except AttributeError:
        print('no a_option in args')
    try:
        print('b_option: ' + str(args.b_option))
    except AttributeError:
        print('no b_option in args')
    try:
        print('c_option: ' + str(args.c_option))
    except AttributeError:
        print('no c_option in args')
    try:
        print('d_option: ' + str(args.d_option))
    except AttributeError:
        print('no d_option in args')
    try:
        print('e_option: ' + str(args.e_option))
    except AttributeError:
        print('no e_option in args')
    try:
        print('f_option: ' + str(args.f_option))
    except AttributeError:
        print('no f_option in args')

if __name__ == '__main__':
    main()