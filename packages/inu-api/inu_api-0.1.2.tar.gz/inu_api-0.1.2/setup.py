from setuptools import setup, Extension

setup(
    name='inu_api',
    version='0.1.2',
    packages=['inu_api'],
    ext_modules=[
        Extension('inu_api.InuStreamsPyth', ['inu_api/InuStreamsPyth.pyd'])
    ],
    install_requires=[
        # Your package dependencies go here
    ],
    # Other metadata like author, description, etc.
)
