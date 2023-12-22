from setuptools import setup, find_packages

import os
import glob

#----------------------------------------------
def is_code(file_path):
    try:
        with open(file_path) as ifile:
            ifile.read()
    except:
        return False

    return True
#----------------------------------------------
def get_scripts(dir_path):
    l_obj = glob.glob(f'{dir_path}/*')
    l_scr = [ obj for obj in l_obj if is_code(obj)]

    return l_scr
#----------------------------------------------
setup(
        name              = 'rk_extractor',
        version           = '0.4.8',
        description       = 'Used to extract RK from simultaneous fits',
        scripts           = get_scripts('scripts/jobs') + get_scripts('scripts/offline'),
        long_description  = '',
        package_dir       = {'' : 'src'},
        packages          = ['', 'extractor_data'],
        package_data      = {'extractor_data' : ['*/*.json']},
        install_requires  = open('requirements.txt').read().splitlines()
        )

