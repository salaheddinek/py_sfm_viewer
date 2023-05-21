#!/usr/bin/env python3
import zipapp
import sys
import shutil
import re
import pathlib

APP_NAME = "py_sfm_viewer"
ADD_VERSION_AS_SUFFIX = True


def get_app_full_name(i_app_path):
    name = APP_NAME
    if ADD_VERSION_AS_SUFFIX:
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


if __name__ == '__main__':
    main_path = pathlib.Path(sys.modules['__main__'].__file__).parents[1]
    deploy_path = main_path / 'deploy'
    app_path = main_path / 'src'

    app_name = get_app_full_name(app_path / "_version.py")


    if deploy_path.is_dir():
        shutil.rmtree(str(deploy_path))
    deploy_path.mkdir(parents=True)

    zipapp.create_archive(app_path, str(deploy_path / (app_name + ".pyz")), '/usr/bin/python3',
                          filter=is_file_accepted)

    print(f"wrapping finished! Output file: {app_name}.pyz")
