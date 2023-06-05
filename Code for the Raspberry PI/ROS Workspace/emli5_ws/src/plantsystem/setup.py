from setuptools import setup

package_name = 'plantsystem'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Emli Group 5',
    maintainer_email='frdur16@student.sdu.dk',
    description='Plant watering system',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pi_node = plantsystem.pi_node:main',
            'farmer_node = plantsystem.farmer_node:main',
            'wateringsystem_node = plantsystem.wateringsystem_node:main'
        ],
    },
)
