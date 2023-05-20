#!/usr/bin/python3
import argparse
import config


def run_with_gui(args, params):
    try:
        import gui
        v_gui = gui.ViewerGui(args, params)
        print("not implemented yet")
    except ImportError:
        raise ImportError('PySide6 python module needs to be installed to use the viewer gui')


def run_with_command_line(args, params):
    if args.subsample_mode == -1:
        return config.CameraSubsampleMode.print_subsample_modes_help_message()
    if args.view_mode == -1:
        return config.ViewMode.print_view_modes_help_message()
    config.DataConsistency.check_view_mode(args.view_mode)
    config.DataConsistency.check_subsample_mode(args.subsample_mode)
    config.DataConsistency.check_color(args.)
    print("nice !")


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
    params = config.get_params()
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='parse camera poses from a txt file with TUM format, and outputs '
                                                 'a trajectory plot as .ply file')
    parser.add_argument('-i', '--input', help='path to the trajectory file in TUM format',
                        type=str, metavar='\b', default="")
    parser.add_argument('-o', '--output', help='path to the output trajectory plot .ply file',
                        type=str, metavar='\b', default="")
    parser.add_argument('-v', '--view_mode', help='the view mode of the camera trajectory plot, possible values: '
                                                  '' + config.ViewMode.get_view_modes_listing(),
                        type=int, metavar='\b', default=params["view_mode"].value)
    parser.add_argument('-s', '--subsample_mode', help='the subsample mode dictates the policy of how frequent a camera'
                                                       ' cone is plotted, possible values:'
                                                       ' ' + config.CameraSubsampleMode.get_subsample_modes_listing(),
                        type=int, metavar='\b', default=params["camera_subsample_mode"].value)
    parser.add_argument('-f', '--factor', help='the camera subsample factor, the behavior of this parameter is linked '
                                               'to the subsample mode chosen by the user',
                        type=float, metavar='\b', default=params["camera_subsample_factor"])
    parser.add_argument()
    parser.add_argument('-g', '--gui', help='display a gui to choose parameters (PySide6 needs to be installed)',
                        type=str2bool, metavar='\b', default=False)
    args = parser.parse_args()
    if args.gui:
        run_with_gui(args, params)
    else:
        run_with_command_line(args, params)


if __name__ == '__main__':
    main()
