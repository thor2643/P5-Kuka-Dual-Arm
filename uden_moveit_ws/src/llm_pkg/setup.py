from setuptools import find_packages, setup

package_name = 'llm_pkg'

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
    maintainer='silas',
    maintainer_email='silasjensen2001@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
        'speech_services = llm_pkg.speech_services_node:main',
        'llm_node = llm_pkg.llm_node:main',
        ],
    },
)
