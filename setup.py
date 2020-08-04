from setuptools import setup

setup(
    name='snapshotalyzer-Shruthi',
    version='0.1',
    author="Shruthi Kulal",
    author_email="Shruthi.Kulal891@outlook.com",
    description="SnapshotAlyzer is a tool to manage EC2 snapshots",
    license="GPLv3+",
    packages=['shotty'],
    url="https://github.com/ShruthiKulal891/snapshotalyzer-Shruthi",
    install_requires=[
        'boto3',
        'click'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    ''',

)