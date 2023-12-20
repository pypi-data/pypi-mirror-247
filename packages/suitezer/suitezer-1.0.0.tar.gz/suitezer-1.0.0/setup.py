from setuptools import setup


setup(
    name="suitezer",
    version="1.0.0",
    packages=['suitezer'],
    entry_points = {
        'console_scripts': [
            'suitezer = suitezer:main',
        ],
    }
)
