from setuptools import setup, find_packages

setup(
    name='magnifai-aut-magnifai-aut-magnifai_aut_sdk-python-python',
    version='0.0.3',
    packages=['magnifai_aut_sdk'],
    install_requires=[
        'iniconfig==2.0.0',
        'jsonpath==0.82.2',
        'pytest==7.4.1',
        'requests==2.31.0',
        'urllib3==2.0.4',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    url='https://github.com/magnifai-gbx/aut-sdk-python',
    author='alejandro.rm',
    author_email='alejandro.rm@globant.com',
    description='Aut magnifai SDK'
)
