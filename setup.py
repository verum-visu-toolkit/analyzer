from distutils.core import setup

setup(
    name='vvanalyzer',
    version='0.0.2',
    packages=['vvanalyzer'],
    url='https://github.com/verum-visu-toolkit/vvanalyzer',
    license='MIT',
    author='Jacob Zimmerman (jczimm)',
    author_email='jczimm@jczimm.com',
    description='Analyzer in verum visu Toolkit',
    install_requires=[
        'numpy==1.13.1',
        'SoundFile==0.9.0.post1',
        'vvsptfile'
    ],
    entry_points={
        'console_scripts': ['vv-analyzer = vvanalyzer.__main__:main']
    }
)
