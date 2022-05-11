from setuptools import setup

setup(
    name="censusbatchgeocoder",
    version="0.0.17",
    description="A simple Python wrapper for U.S. Census Geocoding Services API batch service",
    author="Ben Welsh",
    author_email="b@palewi.re",
    url="http://www.github.com/datadesk/python-censusbatchgeocoder/",
    license="MIT",
    packages=("censusbatchgeocoder",),
    test_suite="tests",
    include_package_data=True,
    install_requires=("requests", "agate>=1.6.0"),
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
    ),
)
