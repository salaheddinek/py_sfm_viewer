#!/usr/bin/env python3
import zipapp
import sys
import shutil
import re
import pathlib
import argparse

APP_NAME = "py_sfm_viewer"


def get_app_full_name(i_app_path, in_add_version_as_suffix):
    name = APP_NAME
    if in_add_version_as_suffix:
        with i_app_path .open("r") as file_obj:
            txt = file_obj.read()
            v_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
            version = re.search(v_re, txt, re.M)
            if version:
                name += "_v" + version.group(1)
    return name


def is_file_accepted(i_file_path):
    if i_file_path.suffix == ".py":
        return True
    return False


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'on', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'off', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected, possible values: yes, y, true, 1, no, n, false, 0.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='bundle the project files into one python file (pyz file) which '
                                                 'can be copied  and used from anywhere in the system')
    parser.add_argument('-s', '--add_suffix', help='add the version number as a suffix to the bundled file',
                        type=str2bool, metavar='\b', default=False)
    args = parser.parse_args()
    main_path = pathlib.Path(sys.modules['__main__'].__file__).parents[1]
    deploy_path = main_path / 'deploy'
    src_path = main_path / 'src'

    app_name = get_app_full_name(src_path / "_version.py", args.add_suffix) + ".pyz"

    bundled_app_path = deploy_path / app_name

    if deploy_path.is_dir():
        shutil.rmtree(str(deploy_path))
    deploy_path.mkdir(parents=True)

    zipapp.create_archive(src_path, str(bundled_app_path), '/usr/bin/python3',
                          filter=is_file_accepted)

    print(f"wrapping finished! Output file: {str(bundled_app_path)}")
