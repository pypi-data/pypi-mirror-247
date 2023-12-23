from setuptools import setup

setup(
    name="django-redis-cache-qube",
    url="http://github.com/qube_money/django-redis-cache/",
    author="Qube Money",
    author_email="admin@qubemoney.com",
    version="3.0.3",
    license="BSD",
    packages=["redis_cache", "redis_cache.backends"],
    description="Redis Cache Backend for Django",
    install_requires=['redis'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
    ],
)
