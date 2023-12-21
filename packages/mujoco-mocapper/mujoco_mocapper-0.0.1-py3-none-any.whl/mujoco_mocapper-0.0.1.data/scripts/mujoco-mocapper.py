import argparse
from mujoco_mocapper import run_mocap_maker, show_xml_keyboard_ctrl

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('xml_file', type=str, help='XML file to mocap')
    parser.add_argument('mocap_body_name', type=str, help='Name of body to attach mocap to')
    parser.add_argument('output_file', type=str, help='Output file')

    args = parser.parse_args()
    xml_file_arg = args.xml_file
    mocap_body_name_arg = args.mocap_body_name
    output_file_arg = args.output_file

    run_mocap_maker(xml_file_arg, mocap_body_name_arg, output_file_arg)

    show_xml_keyboard_ctrl(output_file_arg)
