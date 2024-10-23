from setuptools import find_packages, setup

package_name = 'move_robot'

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
    maintainer='signe',
    maintainer_email='signeskuldbol@hotmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'service = move_robot.joint_values_server:main', 
            'client = move_robot.joint_values_client:main', 
            'test = move_robot.test_joint_values_server:main',
        ],
    },
)
