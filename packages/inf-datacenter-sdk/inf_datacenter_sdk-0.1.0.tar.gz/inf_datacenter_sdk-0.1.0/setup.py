from setuptools import setup, find_packages
import datacenter

def get_requirements():
    import os
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        requires.append(pkg)
    return requires


setup(
    name='inf_datacenter_sdk',
    version= datacenter.__version__,
    packages=find_packages(),
    install_requires=get_requirements(),
    author='zexiang'
)