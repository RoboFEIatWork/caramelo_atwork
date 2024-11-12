from setuptools import setup, find_packages

package_name = 'navegacao_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='atwork',
    maintainer_email='robofei.atwork@gmail.com',
    description='Pacote para controle de robô via serial',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Aqui, você registra os scripts para que possam ser executados pelo ROS 2
            'serial_node_arduino = navegacao_pkg.serial_node_arduino:main',  # Registra o script serial_node_arduino.py
        ],
    },
)
