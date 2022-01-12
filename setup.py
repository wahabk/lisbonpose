from setuptools import setup, find_packages

# TODO use setup.py or setup.cfg?

setup(
       # the name must match the folder name 'verysimplemodule'
        name="lisbonpose", 
        version='0.1.0',
        author="Abdelwahab Kawafi",
        author_email="<akawafi3@gmail.com>",
        description='My PhD project to track foot position for gait analysis.',
        # long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'lisbonpose'],

)