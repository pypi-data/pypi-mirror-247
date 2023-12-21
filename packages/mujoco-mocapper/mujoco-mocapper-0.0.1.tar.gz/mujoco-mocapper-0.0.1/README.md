# Mujoco Mocapper

This is a simple tool and library that takes an mujoco XML file and then adds mocap to a specified body.

The main use case for this is to automate the process since bodies and mocap positions are in different coordinate systems and it is easy to make a mistake when doing this manually.

## Usage

The main usage is through the command line tool. You can install it with `pip install mujoco-mocapper` and then run it with `mujoco-mocapper --help`.

To use this tool, run

```bash
mujoco-mocapper <input_xml> <body_name> <output_xml>
```

where `<input_xml>` is the path to the input mujoco XML file, `<body_name>` is the name of the body to weld the mocap to, and `<output_xml>` is the path to the output mujoco XML file.

