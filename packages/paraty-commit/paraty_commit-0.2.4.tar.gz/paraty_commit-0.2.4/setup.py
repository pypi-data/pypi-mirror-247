
from setuptools import setup
from setuptools.command.install import install

class custom_install_code(install):
    def run(self):
        install.run(self)

setup(
    name='paraty_commit',
    version='0.2.4',
    description='Una biblioteca personalizada',
    author='José Luis Villada',
    author_email='jlvillada@paratytech.com',
    cmdclass={
        'install': custom_install_code
      },
    packages=['paraty_commit'],
    install_requires=['colorama', 'pylint==2.15.10', 'rich'],
    # package_data={'paraty_commit_jlvillada': ['*', '.pre-commit-config.yaml']}
    include_package_data=True,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'paraty_commit = paraty_commit.precommit:main',
        ],
    },
)