from setuptools import setup, find_packages

setup(
    name='naverauth',
    version='0.1.4',
    description='Naver Login Implementation',
    author='stateofai',
    author_email='tellme@duck.com',
    url='https://github.com',
    install_requires=[
        'requests',
        'bs4',
        'lxml',
        'pyc',
        'rsa',
        'urllib3',
        'json',
        'base64',
        'time',
        'datetime',
        'random',
    ],
    packages=find_packages(exclude=[]),
    keywords=['clien', 'naver'],
    python_requires='>=3.9',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)
