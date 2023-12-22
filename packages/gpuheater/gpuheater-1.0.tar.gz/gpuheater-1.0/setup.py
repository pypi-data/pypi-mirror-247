from setuptools import setup

setup(
    name='gpuheater',
    version='1.0',
    description='A Python package running full of GPUs for heating',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="sword4869",
    url='https://github.com/sword4869/gpuheater',
    license='MIT License',
    install_requires=[
        'torch',
        'argparse',
        'nvitop'
    ],
    dependency_links=[
        'https://download.pytorch.org/whl/cu101/torch-1.5.1%2Bcu101-cp36-cp36m-linux_x86_64.whl'
    ],
    entry_points={
        'console_scripts':[
            'gpuheater = gpuheater.core:main'
        ]
    }
)