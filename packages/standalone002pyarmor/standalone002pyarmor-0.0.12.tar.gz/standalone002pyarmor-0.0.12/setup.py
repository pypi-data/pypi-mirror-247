
from setuptools import setup, find_packages

setup(
    name='standalone002pyarmor',
    version='0.0.12',
    packages=find_packages(),
    package_data={
         'standalone002pyarmor': [
         'exfn001add.py', 
         'dist/exfn001add_release.py',
         'dist/pytransform/*'],
    },
    # install_requires=open('requirements.txt').read().splitlines(),
    install_requires=[
        # 'SomePackage==1.2.3',
        # 更多依赖项...
    ],
    description='一个 Python 混淆工具包',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='xiaowen',
    author_email='xiaowenseekjob@gmail.com',
    url='https://github.com/yourusername/standalone001pyarmor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
