import mujoco
import xml.etree.ElementTree as ET

from .xml_view import show_xml, show_xml_keyboard_ctrl


def get_first_body_pos(xml_file, mocap_body_name):
    """
    Run mujoco with the xml_file and find the position and quaternion of the mocap_body_name
    :param xml_file:
    :param mocap_body_name:
    :return:
    """
    # Load the model
    model = mujoco.MjModel.from_xml_path(xml_file)
    data = mujoco.MjData(model)
    mujoco.mj_kinematics(model, data)

    # Get the body position
    body_id = model.body(name=mocap_body_name).id
    body_pos = data.xpos[body_id]
    body_quat = data.xquat[body_id]

    return body_pos, body_quat


def run_mocap_maker(xml_file, mocap_body_name, output_file):
    """
    Run the mocap maker

    The steps are as follows:
    1. Run mujoco with the xml_file and find the position of the mocap_body_name
    2. Write the output_file with the mocap_body_name position

    :param xml_file: Input XML file
    :param mocap_body_name: Name of body to attach mocap to
    :param output_file: Output XML file
    :return: None
    """

    body_pos, body_quat = get_first_body_pos(xml_file, mocap_body_name)

    # Open the input file as an XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    worldbody = root.find('worldbody')

    # Add mocap body to the root
    body_pos_str = ' '.join([str(x) for x in body_pos])
    body_quat_str = ' '.join([str(x) for x in body_quat])
    mocap_body = ET.SubElement(worldbody, 'body', mocap='true', name='mocap', pos=body_pos_str,
                               quat=str(body_quat_str))
    # Add the sites to the mocap body
    ET.SubElement(mocap_body, 'site', pos="0 0 0.075", size="0.003 0.003 0.1", type="box", name='mocap_site1',
                  rgba="0 0 1 1")
    ET.SubElement(mocap_body, 'site', pos="0 0.075 0", size="0.003 0.1 0.003", type="box", name='mocap_site2',
                  rgba="0 1 0 1")
    ET.SubElement(mocap_body, 'site', pos="0.075 0 0", size="0.1 0.003 0.003", type="box", name='mocap_site3',
                  rgba="1 0 0 1")

    # Add the weld joint to the mocap body
    equality_body = ET.SubElement(root, 'equality')
    ET.SubElement(equality_body, 'weld', body1='mocap', body2=mocap_body_name)

    # Write the output file. No pretty formatting available with this library :(.
    tree.write(output_file, method="xml")