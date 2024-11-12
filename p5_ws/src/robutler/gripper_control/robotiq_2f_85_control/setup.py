from setuptools import find_packages, setup

package_name = 'robotiq_2f_85_control'

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
    maintainer='thor',
    maintainer_email='thor951753@hotmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gripper_control_service_node = robotiq_2f_85_control.gripper_service:main',
            'gripper_client_node = robotiq_2f_85_control.gripper_client:main',
        ],
    },
)
