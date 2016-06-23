from setuptools import setup, find_packages

setup(
    name='aiologin',
    version='0.0.1',
    description='sessions for aiohttp.web',
    long_description='',
    url='https://github.com/trivigy/aiologin',
    license='MIT',
    author='Konstantin Itskov',
    author_email='konstantin.itskov@kovits.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP'
    ],
    install_requires=[
        'aiohttp>=0.21.6',
        'aiohttp_session>=0.5.0'
    ],
    packages=find_packages(exclude=['tests*'])
)
