from setuptools import setup, find_packages

setup(
    name='standalone003gntmcallmln',
    version='0.0.7',
    packages=find_packages(),
    package_data={
        'standalone003gntmcallmln_dist': [
        'kangroll_basic_fn001_mln',
        'kangroll_basic_fn001_mln_release.py',
        'pytransform/*'],
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
