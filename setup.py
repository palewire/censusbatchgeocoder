import os

from setuptools import setup


def read(file_name):
    """Read the provided file."""
    this_dir = os.path.dirname(__file__)
    file_path = os.path.join(this_dir, file_name)
    with open(file_path) as f:
        return f.read()


def version_scheme(version):
    """Version scheme hack for setuptools_scm.
    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342
    If that issue is resolved, this method can be removed.
    """
    import time

    from setuptools_scm.version import guess_next_version

    if version.exact:
        return version.format_with("{tag}")
    else:
        _super_value = version.format_next_version(guess_next_version)
        now = int(time.time())
        return _super_value + str(now)


def local_version(version):
    """Local version scheme hack for setuptools_scm.
    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342
    If that issue is resolved, this method can be removed.
    """
    return ""


setup(
    name="censusbatchgeocoder",
    description="A simple Python wrapper for the U.S. Census Geocoding Services API batch service",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Ben Welsh",
    author_email="b@palewi.re",
    url="http://www.github.com/palewire/censusbatchgeocoder/",
    license="MIT",
    packages=("censusbatchgeocoder",),
    test_suite="tests",
    install_requires=("requests", "agate>=1.6.0"),
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
    ),
    setup_requires=["setuptools_scm"],
    use_scm_version={"version_scheme": version_scheme, "local_scheme": local_version},
    project_urls={
        "Documentation": "http://palewi.re/docs/censusbatchgeocoder",
        "Source": "https://github.com/palewire/censusbatchgeocoder",
        "Tracker": "https://github.com/palewire/censusbatchgeocoder/issues",
    },
)
