from setuptools import setup, find_packages

setup(
    name='standalone002pyarmor',
    version='0.0.21',
    packages=find_packages(),
    package_data={
        'standalone002pyarmor': ['standalone002pyarmor/dist/exfn001add_release.py', 'standalone002pyarmor/dist/pytransform/*'],
    },
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
