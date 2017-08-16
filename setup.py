from distutils.core import setup

setup(
    name='vvanalyzer',
    version='0.0.1',
    packages=['analyzer'],
    url='https://github.com/verum-visu-toolkit/analyzer',
    license='MIT',
    author='Jacob Zimmerman (jczimm)',
    author_email='jczimm@jczimm.com',
    description='Analyzer in verum visu Toolkit',
    scripts=['bin/vv-analyzer'],
    install_requires=[
        'numpy==1.13.1',
        'SoundFile==0.9.0.post1'
    ]
)
