from setuptools import setup

setup(
    name='clidogut',
    version='1.0.1',
    py_modules=['clidogut'],
    install_requires=['Click', ],
    entry_points={
        'console_scripts': [
            'clidogut = clidogut:cli'
        ]
    }
)
