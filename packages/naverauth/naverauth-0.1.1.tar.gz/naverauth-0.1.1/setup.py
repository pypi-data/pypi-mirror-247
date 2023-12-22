from setuptools import setup, find_packages

setup(
    name='naverauth',
    version='0.1.1',
    description='Naver Login Implementation',
    author='stateofai',
    author_email='tellme@duck.com',
    url='https://github.com',
    install_requires=['uuid', 'requests','rsa','lzstring','Retry','HTTPAdapter',],
    packages=find_packages(exclude=[]),
    keywords=['clien', 'naver'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)
