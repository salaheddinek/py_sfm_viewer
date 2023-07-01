#!/usr/bin/env python3
import sys
import shutil
import PyInstaller.__main__
import re
import pathlib
import tarfile
import stat

APP_NAME = "sfm_viewer"
SHELL_CONtENT = f"""#!/bin/sh

dir_path=$(dirname $(realpath $0));
app_path="$dir_path/{APP_NAME}/{APP_NAME}";

# create a '.desktop' file if it does not exists or if path has changed
create_desktop_shortcut()
{{
    short_cut_path="$dir_path/{APP_NAME}.desktop";
    icon_path="$dir_path/{APP_NAME}/{APP_NAME}.png"
    if [ -e $short_cut_path ]; then
        if  grep -q "$icon_path" "$short_cut_path" ; then
            return ;
        fi
    fi
    rm -f $short_cut_path;
    touch $short_cut_path;
    chmod +x $short_cut_path;
    echo "[Desktop Entry]" >> $short_cut_path
    echo "Comment=parse camera poses from a txt file with TUM format, and outputs a trajectory plot as .ply file" >> $short_cut_path
    echo "Exec=$app_path" >> $short_cut_path
    echo "Icon=$icon_path" >> $short_cut_path
    echo "Name=sfm_viewer" >> $short_cut_path
    echo "StartupNotify=true" >> $short_cut_path
    echo "Terminal=false" >> $short_cut_path
    echo "Type=Application" >> $short_cut_path
    echo "Version=1.0" >> $short_cut_path
}}

create_desktop_shortcut
"$app_path" $@;
"""


def get_app_full_name(i_version_file_path):
    name = APP_NAME
    with i_version_file_path.open("r") as file_obj:
        txt = file_obj.read()
        v_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
        version = re.search(v_re, txt, re.M)
        if version:
            name += "_v" + version.group(1)
    return name


def deploy_command(i_deploy_path, i_src_path, i_build_path):
    cmd = [str(i_src_path), "-n", APP_NAME, "--clean", "--distpath", str(i_deploy_path),
           "--workpath", str(i_build_path / "build"), "--specpath", str(i_build_path)]
    # print("Build command:\n\n{}\n\n".format(" ".join(cmd)) )
    PyInstaller.__main__.run(cmd)


def main():
    if sys.platform.lower() == "win32":
        print("ERROR: this deployment script is not suitable for Windows")
        exit(1)

    main_path = pathlib.Path(sys.modules['__main__'].__file__).parents[1]
    name_w_version = get_app_full_name(main_path / 'src' / "_version.py")
    src_path = main_path / 'src' / '__main__.py'
    deploy_parent_path = main_path / 'deploy'
    deploy_path = deploy_parent_path / name_w_version
    shell_script_path = deploy_path / f"start_{APP_NAME}.sh"
    icon_dst_path = deploy_path / APP_NAME / f"{APP_NAME}.png"
    icon_src_path = main_path / "images" / f"{APP_NAME}.png"

    # ----+ deployment folder creation -----+
    print("Deployment path: {}".format(deploy_path))
    if deploy_parent_path.is_dir():
        shutil.rmtree(deploy_parent_path)
    deploy_parent_path.mkdir(parents=True)

    # ----+ freeze command -----+
    deploy_command(deploy_path, src_path, deploy_parent_path)

    # ----+ finish bundling -----+
    with shell_script_path.open("w") as file_obj:
        file_obj.write(SHELL_CONtENT)
        print(f"saved shell script to: {shell_script_path}")
    shell_script_path.chmod(shell_script_path.stat().st_mode | stat.S_IEXEC)

    shutil.copy(str(icon_src_path), str(icon_dst_path))
    print(f"copied icon from [{str(icon_src_path)}] to [{str(icon_dst_path)}]")

    print("compressing app files ...")
    with tarfile.open(str(deploy_path) + "_linux.tar.gz", "w:gz") as tar:
        tar.add(str(deploy_path), arcname=name_w_version)
    print('compression finished')


if __name__ == '__main__':
    main()
