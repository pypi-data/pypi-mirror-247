from setuptools import setup, find_packages

setup(
    name='flask-session-custom',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "flask>=2.2",
        "cachelib",
        "itsdangerous",
        "Werkzeug"
    ],
)
