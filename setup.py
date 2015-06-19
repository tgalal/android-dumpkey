deps = ['M2Crypto']
from setuptools import setup, find_packages
import dumpkey
setup(
    name='android-dumpkey',
    version=dumpkey.__version__,
    url='http://github.com/tgalal/android-dumpkey/',
    license='Apache License, Version 2.0',
    author='Tarek Galal',
    tests_require=[],
    install_requires = deps,
    scripts = ['dumppublickey'],
    author_email='tare2.galal@gmail.com',
    description='Python port of com.android.dumpkey.DumpPublicKey',
    #long_description=long_description,
    packages= find_packages(),
    include_package_data=True,
    platforms='any',
    #test_suite='',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
        ]
)