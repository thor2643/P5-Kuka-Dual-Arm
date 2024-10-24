from setuptools import find_packages, setup

package_name = 'bimanuel_gripper_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kazzi',
    maintainer_email='kkl@stofanet.dk',
    description='Client for RobotIQ 3f control, aims to allow LLM to control gripper',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'client3f = bimanuel_gripper_control.3f_client:main',
        	'client2f = bimanuel_gripper_control.2f_client:main',
        	'service2f = bimanuel_gripper_control.2f_service:main',
        ],
    },
)
