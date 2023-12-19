from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='sherlock_lib',
    version='0.1.3',
    license='MIT License',
    author='Paulo Ricardo Mesquita',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='pauloricardomrs2002@gmail.com',
    keywords='sherlock, stalking, sherlock lib, sherlock-lib,stalking lib, stalking-lib,stalking with sherlock',
    description=u'🔎 Hunt down social media accounts by username across social networks',
    packages=find_packages(),
    install_requires=[
        'certifi==2019.6.16',
        'PySocks==1.7.0',
        'requests==2.22.0',
        'requests-futures==1.0.0',
        'stem==1.8.0',
        'exrex==0.11.0',
    ],
)
