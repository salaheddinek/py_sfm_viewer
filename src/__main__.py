#!/usr/bin/python3
import argparse
import config
import color
import geometry_builder
import sys


def intro_print(in_art):
    """ Taken from https://patorjk.com/software/taag using 4MAX font"""
    intro = """
    .dP"Y8 888888 8b    d8     Yb    dP 88 Yb        dP 888888 88""Yb 
    `Ybo." 88__   88b  d88      Yb  dP  88  Yb  db  dP  88__   88__dP 
    o.`Y8b 88""   88YbdP88       YbdP   88   YbdPYbdP   88""   88"Yb  
    8bodP' 88     88 YY 88        YP    88    YP  YP    888888 88  Yb
    """
    if in_art:
        print(intro)
    print((" SFM viewer ".center(80, "=")))
    print("")


def end_print(in_art):
    end = """
               ,d8PPPP 888  ,d8   88PPP.            
    ______     d88ooo  888_dPY8   88   8     ______ 
    XXXXXX   ,88'      8888' 88   88   8     XXXXXX 
             88bdPPP   Y8P   Y8   88oop'               
    """
    print("")
    print((" SFM viewer: done! ".center(80, "=")))
    if in_art:
        print(end)


def run_with_gui(args, params):
    try:
        import ui_core
        import PySide6.QtWidgets as Qw
        app = Qw.QApplication(sys.argv)
        app.setStyle("Fusion")
        window = ui_core.ViewerGui(args, params)

        window.show()
        sys.exit(app.exec())
    except ImportError:
        raise ImportError('PySide6 python module needs to be installed to use the viewer gui')


def run_with_command_line(args, params):
    if args.subsample_mode == -1:
        print(config.CameraSubsampleMode.get_subsample_modes_help_message())
        return
    if args.view_mode == -1:
        print(config.ViewMode.get_view_modes_help_message())
        return

    # verifications
    config.DataConsistency.check_view_mode(args.view_mode)
    config.DataConsistency.check_subsample_mode(args.subsample_mode)
    config.DataConsistency.check_positive_float("camera cone size",args.cone_size)
    config.DataConsistency.check_positive_float("camera subsample factor", args.factor)
    first_color = color.Color.parse_from_str(args.first_color)
    last_color = color.Color.parse_from_str(args.last_color)
    params.update_used_colormap(args.colormap)

    # params update
    params.input_path = args.input
    params.output_path = args.output
    params.configuration["view_mode"] = config.ViewMode(args.view_mode)
    params.configuration["camera_cone_size"] = args.cone_size
    params.configuration["camera_subsample_mode"] = config.CameraSubsampleMode(args.subsample_mode)
    params.configuration["camera_subsample_factor"] = args.factor
    params.configuration["first_camera_color"] = first_color.to_str(True)
    params.configuration["last_camera_color"] = last_color.to_str(True)
    params.configuration["display_ascii_art"] = args.art

    intro_print(args.art)
    params.process_output_path()
    params.print_info()
    viewer = geometry_builder.GeometryBuilder(params)
    viewer.write_camera_trajectory_plot()
    end_print(args.art)
    params.save_to_config_file()

    # for i, theme in enumerate(params.configuration["available_colormaps"]):
    #     params.configuration["colormap_used"] = theme
    #     params.output_path = f'{i}.ply'


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected, possible values: yes, y, true, 1, no, n, false, 0.')


def main():
    params = config.Params()
    params.load_from_config_file_if_possible()
    # params.delete_config_file_if_exists()
    # print("config file path: " + str(config.Params.get_config_file_path()))
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='parse camera poses from a txt file with TUM format, and outputs '
                                                 'a trajectory plot as .ply file')
    parser.add_argument('-i', '--input', help='path to the trajectory file in TUM format',
                        type=str, metavar='\b', default="")
    parser.add_argument('-o', '--output', help='path to the output trajectory plot .ply file',
                        type=str, metavar='\b', default="")
    parser.add_argument('-g', '--gui', help='display a gui to choose parameters (PySide6 needs to be installed)',
                        type=str2bool, metavar='\b', default=False)
    parser.add_argument('-v', '--view_mode', help='the view mode of the camera trajectory plot, possible values: '
                                                  '' + config.ViewMode.get_view_modes_listing(),
                        type=int, metavar='\b', default=params.configuration["view_mode"].value)
    parser.add_argument('-n', '--cone_size', help='the camera cone height',
                        type=float, metavar='\b', default=params.configuration["camera_cone_size"])
    parser.add_argument('-s', '--subsample_mode', help='the subsample mode dictates the policy of how frequent a camera'
                                                       ' cone is plotted, possible values:'
                                                       ' ' + config.CameraSubsampleMode.get_subsample_modes_listing(),
                        type=int, metavar='\b', default=params.configuration["camera_subsample_mode"].value)
    parser.add_argument('-t', '--factor', help='the camera subsample factor, the behavior of this parameter is linked '
                                               'to the subsample mode chosen by the user',
                        type=float, metavar='\b', default=params.configuration["camera_subsample_factor"])
    parser.add_argument('-m', '--colormap', help='the color map to use for the camera cone colors. If left as custom,'
                                                 ' then cone color is interpolated between first and last camera color.'
                                                 ' Available colormaps: ' + params.available_color_maps(),
                        type=str, metavar='\b', default=params.configuration["colormap_used"])
    parser.add_argument('-f', '--first_color', help='first camera color, both HEX and RGB formats are accepted'
                                                    ' (neglected if colormap is not set to custom)',
                        type=str, metavar='\b', default=params.configuration["first_camera_color"])
    parser.add_argument('-l', '--last_color', help='last camera color, both HEX and RGB formats are accepted'
                                                   ' (neglected if colormap is not set to custom)',
                        type=str, metavar='\b', default=params.configuration["last_camera_color"])
    parser.add_argument('-a', '--art', help='Display ASCII art',
                        type=str2bool, metavar='\b', default=params.configuration["display_ascii_art"])
    args = parser.parse_args()
    if args.gui:
        run_with_gui(args, params)
    else:
        run_with_command_line(args, params)


if __name__ == '__main__':
    main()
