from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='flask-session-custom',
    version='0.1.1',
    packages=find_packages(where='src'),
    description='Your short project description here',
    long_description=long_description,  # Sử dụng nội dung củ
    long_description_content_type='text/markdown',
    author='Thang Tran',
    author_email='thangtd1993@gmail.com',
    package_dir={'': 'src'},
    install_requires=[
        "flask>=2.2",
        "cachelib",
        "itsdangerous",
        "Werkzeug"
    ],
)
