from setuptools import find_packages, setup
from glob import glob

package_name = 'template_python_step_5_include_data'

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
        # Include data files
        ('share/' + package_name + '/data',
            glob('data/*')),
        # Include AI model files
        ('share/' + package_name + '/models',
            glob('models/*'))
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
            'image_publisher_node = template_python_step_5_include_data.image_publisher_node:main',
            'inference_node = template_python_step_5_include_data.inference_node:main',
            'result_viewer_node = template_python_step_5_include_data.result_viewer_node:main',
        ],
    },
)
