from setuptools import setup, find_packages

long_description = "Tool for adding mocap to mujoco models"

setup(
    name='mujoco-mocapper',
    version='0.0.1',
    description='Tool for adding mocap to mujoco models',
    author='Mochan Shrestha',
    packages=['mujoco_mocapper'],
    install_requires=[
        'mujoco',
        'pyquaternion',
        'pytest'
    ],
    long_description=long_description,
    scripts=['bin/mujoco-mocapper'],
)
