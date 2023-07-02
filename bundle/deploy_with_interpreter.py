#!/usr/bin/env python3
import sys
import shutil
import re
import pathlib
import zipfile
import argparse
import zipapp


APP_NAME = "sfm_viewer"


def is_file_accepted(i_file_path):
    if i_file_path.suffix == ".py":
        return True
    return False


def get_app_full_name(i_version_file_path):
    name = APP_NAME
    with i_version_file_path.open("r") as file_obj:
        txt = file_obj.read()
        v_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
        version = re.search(v_re, txt, re.M)
        if version:
            name += "_v" + version.group(1)
    return name


def check_embedded_python_file(in_path: pathlib.Path):
    if not in_path.is_dir():
        return False
    interpreter_path = in_path / "python.exe"
    print(interpreter_path)
    if not interpreter_path.is_file():
        return False
    return True


def create_bat_script(script_path, embedded_python_path):
    content = f"@echo off\n%~dp0{embedded_python_path.name}\\python.exe %~dp0{APP_NAME}.pyz %*"
    with script_path.open("w") as file_obj:
        file_obj.write(content)


def compress_folder(src_path, dst_path):
    # compression method comparison :
    # https://stackoverflow.com/questions/4166447/python-zipfile-module-doesnt-seem-to-be-compressing-my-files
    with zipfile.ZipFile(str(dst_path), mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for content in src_path.rglob("*"):
            if "__pycache__" in content.parts:
                continue
            archive.write(content, content.relative_to(src_path.parent))


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Bundle the project files into one python file (pyz file), and '
                                                 'provide an embedded python interpreter with the needed packages, so '
                                                 'that the application can be run without any installations.')
    parser.add_argument('-e', '--embedded_python', help='path to embedded python interpreter folder',
                        type=str, metavar='\b', required=True)
    args = parser.parse_args()
    src_python_path = pathlib.Path(args.embedded_python)
    if not check_embedded_python_file(src_python_path):
        print("ERROR: provided embedded python folder is in wrong format: " + str(src_python_path))
        exit(1)

    # ----+ paths and names -----+
    main_path = pathlib.Path(sys.modules['__main__'].__file__).parents[1]
    name_w_version = get_app_full_name(main_path / 'src' / "_version.py")
    src_path = main_path / 'src'
    deploy_parent_path = main_path / 'deploy'
    deploy_path = deploy_parent_path / name_w_version
    batch_script_path = deploy_path / f"start_{APP_NAME}.bat"
    dst_python_path = deploy_path / "python_embedded_amd64"

    # ----+ deployment folder creation -----+
    print("Deployment path: {}".format(deploy_path))
    if deploy_parent_path.is_dir():
        shutil.rmtree(deploy_parent_path)
    deploy_path.mkdir(parents=True)

    print("creating script using zip_app ...")
    zipapp.create_archive(src_path, str(deploy_path / (APP_NAME + ".pyz")), '/usr/bin/python3',
                          filter=is_file_accepted)

    print("copying embedded python folder ...")
    shutil.copytree(str(src_python_path), str(dst_python_path), symlinks=True, ignore=None,
                    copy_function=shutil.copy2, ignore_dangling_symlinks=False, dirs_exist_ok=False)

    print("creating launch script ...")
    create_bat_script(batch_script_path, dst_python_path)

    # ----+ compress package -----+
    print("compressing app files ...")
    compress_folder(deploy_path, deploy_parent_path / (name_w_version + "_windows_x64.zip"))
    print("finished !")


if __name__ == '__main__':
    main()
