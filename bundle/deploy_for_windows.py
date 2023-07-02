#!/usr/bin/env python3
import sys
import shutil
import re
import pathlib
import zipfile
import PyInstaller.__main__


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


def compress_folder(src_path, dst_path):
    # compression method comparison :
    # https://stackoverflow.com/questions/4166447/python-zipfile-module-doesnt-seem-to-be-compressing-my-files
    with zipfile.ZipFile(str(dst_path), mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for content in src_path.rglob("*"):
            if "__pycache__" in content.parts:
                continue
            archive.write(content, content.relative_to(src_path))


def deploy_command(i_deploy_path, i_src_path, i_build_path, i_icon_path):
    cmd = [str(i_src_path), "-n", APP_NAME, "--clean", "--distpath", str(i_deploy_path),
           "--workpath", str(i_build_path / "build"), "--specpath", str(i_build_path), "-i", str(i_icon_path)]
    # print("Build command:\n\n{}\n\n".format(" ".join(cmd)) )
    PyInstaller.__main__.run(cmd)


def main():
    # ----+ paths and names -----+
    main_path = pathlib.Path(sys.modules['__main__'].__file__).parents[1]
    name_w_version = get_app_full_name(main_path / 'src' / "_version.py")
    src_path = main_path / 'src' / '__main__.py'
    icon_path = main_path / 'images' / 'sfm_viewer.ico'
    deploy_parent_path = main_path / 'deploy'
    deploy_path = deploy_parent_path / APP_NAME

    # ----+ deployment folder creation -----+
    print("Deployment path: {}".format(deploy_path))
    if deploy_parent_path.is_dir():
        shutil.rmtree(deploy_parent_path)
    deploy_parent_path.mkdir(parents=True)

    # ----+ freeze command -----+
    deploy_command(deploy_path, src_path, deploy_parent_path, icon_path)

    # ----+ compress package -----+
    print("compressing app files ...")
    compress_folder(deploy_path, deploy_parent_path / (name_w_version + "_windows_x64.zip"))
    print("finished !")


if __name__ == '__main__':
    main()
