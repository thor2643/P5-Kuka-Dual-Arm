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
            'fibonacci_action_server = action_tutorials_py.fibonacci_action_server:main', #This needs to be chanced
            'fibonacci_action_client = action_tutorials_py.fibonacci_action_client:main', #This needs to be chanced
        ],
    },
)
