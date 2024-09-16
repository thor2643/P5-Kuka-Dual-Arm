from setuptools import find_packages, setup

package_name = 'robot_controller'

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
    maintainer='kasper',
    maintainer_email='kkla22@student.aau.dk',
    description='Package used for controlling two KUKA LBR IIWA 7 R800s',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'move_world = robot_controller.move_world:main',
        ],
    },
)
