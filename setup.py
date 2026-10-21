"""
My Tool does one thing, and one thing well.
"""
from setuptools import find_packages, setup


def install_deps():
    """Reads requirements.txt and preprocesses it
    to be fed into setuptools.

    This is the only possible way (we found)
    how requirements.txt can be reused in setup.py
    using dependencies from private github repositories.

    Links must be appended by `-{StringWithAtLeastOneNumber}`
    or something like that, so e.g. `-9231` works as well as
    `1.1.0`. This is ignored by the setuptools, but has to be there.

    Returns:
         list of packages and dependency links.
    """
    new_pkgs = []
    links = []
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        for resource in f:
            resource = resource.strip()
            if not resource or resource.startswith('#'):
                continue
            if 'git+https' in resource:
                pkg = resource.split('#')[-1]
                links.append(resource + '-9876543210')
                new_pkgs.append(pkg.replace('egg=', '').rstrip())
            else:
                new_pkgs.append(resource)
    return new_pkgs, links


dependencies, dependency_links = install_deps()

setup(
    name='atf2conllconvertor',
    version='0.2.10',
    url='https://github.com/cdli-gh/atf2conll-convertor',
    license='BSD',
    author='Jayanth',
    author_email='jayanthjaiswal15@gmail.com',
    description='My Tool does one work, and one work well.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.8',
    install_requires=dependencies,
    dependency_links=dependency_links,
    entry_points={
        'console_scripts': [
            'atf2conll = atf2conll_convertor.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
