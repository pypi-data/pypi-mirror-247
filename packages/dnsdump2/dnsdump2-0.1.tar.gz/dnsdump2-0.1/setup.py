from setuptools import setup, find_packages

setup(
    name='dnsdump2',
    version='0.1',
    py_modules=['dnsdump2'],
    install_requires=[
        'requests',
        'tqdm',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'dnsdump2 = dnsdump2:main'
        ]
    },
)
