from setuptools import find_packages, setup
from glob import glob

package_name = 'template_python_step_4_config'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        ('share/' + package_name + '/launch',
            glob('launch/*.launch.py')),
        # Include config files
        ('share/' + package_name + '/config',
            glob('config/*.yaml')),
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
            'listener4 = template_python_step_4_config.listener4:main',
            'talker4 = template_python_step_4_config.talker4:main',
            'talker4_dynamic = template_python_step_4_config.talker4_dynamic:main',
        ],
    },
)
