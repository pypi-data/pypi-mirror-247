from setuptools import setup

setup(
    name='kikicorelib',
    version='0.1.1',
    packages=[],
    entry_points={
        'console_scripts': [
            'mypackage-cli=mypackage.mymodule:main',
        ],
    },
    install_requires=[
        # List your dependencies here
    ],
)
