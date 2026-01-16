from setuptools import find_packages, setup

package_name = 'template_python_step_2'

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
    maintainer='suogi',
    maintainer_email='suogi@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'temp_node = template_python_step_2.temp_node:main',
            'talker_step_2 = template_python_step_2.talker_step_2:main',
            'listener_step_2 = template_python_step_2.listener_step_2:main',
        ],
    },
)
