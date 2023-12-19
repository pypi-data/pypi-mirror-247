from setuptools import setup, find_packages

setup(
    name='jmcwatch',
    version='1.5.6',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jmcwatch=jmcwatch.cli:main',
        ],
    },
    install_requires=[
        'click',
        'watchdog',
        'jmcfunction'
    ],
    dependency_links=[
        'git+https://github.com/WingedSeal/jmc.git@src#egg=jmc'
    ],
    author='amandin',
    author_email='amawwdin@email.com',
    description='Watch and compile JMC files. Simply type `jmcwatch` to use.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)
