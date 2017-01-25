from distutils.core import setup

__packagename__ = "dualprocessing"

def get_version():
    import os, re
    VERSIONFILE = os.path.join(__packagename__, 'broker.py')
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

__version__ = get_version()
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name = __packagename__,
    packages = [__packagename__], # this must be the same as the name above
    version = __version__,
    description = 'This module is designed to help with running a single-instance, thread-blocking computation pipeline on a second process. It does all the heavy lifting of scheduling calls and asynchronously waiting for the results.',
    author = 'Esteban Siravegna, based on works of Michael Osthege',
    author_email = 'esiravegna@gmail.com',
    url = 'https://github.com/esiravegna/dualprocessing', # use the URL to the github repo
    download_url = 'https://github.com/esiravegna/dualprocessing/tarball/%s' % __version__,
    keywords = ['multiprocessing'], # arbitrary keywords
    license = 'MIT',
    install_requires = REQUIREMENTS,
    classifiers= [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Developers"
    ]
)

