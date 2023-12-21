import mujoco
import mujoco.viewer

from .mocap_move import key_callback_data


def show_xml(xml_file):
    # Load the model
    model = mujoco.MjModel.from_xml_path(xml_file)
    data = mujoco.MjData(model)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            mujoco.mj_step(model, data)
            viewer.sync()


def show_xml_keyboard_ctrl(xml_file):
    # Load the model
    model = mujoco.MjModel.from_xml_path(xml_file)
    data = mujoco.MjData(model)

    def key_callback(key):
        key_callback_data(key, data)

    with mujoco.viewer.launch_passive(model, data, key_callback=key_callback) as viewer:
        while viewer.is_running():
            mujoco.mj_step(model, data)
            viewer.sync()
