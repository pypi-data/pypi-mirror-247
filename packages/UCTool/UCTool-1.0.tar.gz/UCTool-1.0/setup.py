from distutils.core import  setup
import setuptools
packages = ['UCTool']# 唯一的包名，自己取名
setup(name='UCTool',
	version='1.0',
	author='xjw',
    packages=packages,
    package_dir={'requests': 'requests'},)
