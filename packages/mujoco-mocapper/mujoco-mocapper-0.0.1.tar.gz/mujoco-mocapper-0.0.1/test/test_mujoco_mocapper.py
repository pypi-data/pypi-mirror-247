import numpy as np
import xml.etree.ElementTree as ET

from mujoco_mocapper.mujoco_mocapper import get_first_body_pos, run_mocap_maker


def test_get_first_body_pos():
    xml_file = 'test_falling_cube.xml'
    mocap_body_name = 'cube'
    body_pos, body_quat = get_first_body_pos(xml_file, mocap_body_name)
    assert np.allclose(body_pos, np.array([0.0, 0.0, 0.2]))
    assert np.allclose(body_quat, np.array([1.0, 0.0, 0.0, 0.0]))


def test_run_mocap_maker():
    output_xml = 'test_falling_cube_mocap.xml'
    run_mocap_maker('test_falling_cube.xml', 'cube', output_xml)

    # Check that it has all the expected elements
    tree = ET.parse(output_xml)
    root = tree.getroot()
    worldbody = root.find('worldbody')
    assert worldbody is not None

    # Find the mocap body
    bodies = worldbody.findall('body')
    assert bodies is not None
    assert len(bodies) == 3

    # Find the body named mocap
    mocap_body = bodies[2]

    assert mocap_body is not None
    assert mocap_body.attrib['name'] == 'mocap'
    assert mocap_body.attrib['mocap'] == 'true'
    assert mocap_body.attrib['pos'] == '0.0 0.0 0.2'
    assert mocap_body.attrib['quat'] == '1.0 0.0 0.0 0.0'

    # Check that the weld joint is there
    weld = root.find('equality/weld')
    assert weld is not None
    assert weld.attrib['body1'] == 'mocap'
    assert weld.attrib['body2'] == 'cube'
