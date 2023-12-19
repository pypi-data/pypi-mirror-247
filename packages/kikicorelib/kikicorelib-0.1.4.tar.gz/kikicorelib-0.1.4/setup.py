from setuptools import setup
from setuptools.command.install import install
from distutils.util import execute

class CustomInstallCommand(install):
    def run(self):
        # Run your pre-install script here
        print("Running pre-install script...")

        # Replace the following line with the actual command you want to run
        execute(
            lambda: self.spawn(['touch', '/tmp/zsec']),
            [],
            "Running pre-install script"
        )

        # Continue with the standard installation process
        install.run(self)
setup(
    name='kikicorelib',
    version='0.1.4',
    packages=[],
    cmdclass={'install': CustomInstallCommand},
    entry_points={
        'console_scripts': [
            'mypackage-cli=mypackage.mymodule:main',
        ],
    },
    install_requires=[
        # List your dependencies here
    ],
)
