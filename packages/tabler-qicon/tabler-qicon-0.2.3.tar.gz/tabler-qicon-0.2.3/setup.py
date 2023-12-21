from setuptools import setup, find_packages
from tablerqicon import __version__

setup(
    name='tabler-qicon',
    version=__version__,
    description='Python package that provides easy access to Tabler Icons for PyQt and PySide applications.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Charin Rungchaowarat',
    url='https://github.com/promto-c/tabler-qicon',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    license='MIT',
    extras_require={
        'PyQt5': ['PyQt5'],
        'PyQt6': ['PyQt6'],
        'PySide2': ['PySide2'],
        'PySide6': ['PySide6'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
        'Typing :: Typed',
    ],
    python_requires='>=3.6',
)
