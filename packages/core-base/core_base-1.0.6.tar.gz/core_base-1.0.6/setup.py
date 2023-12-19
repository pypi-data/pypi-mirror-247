from setuptools import setup, find_packages
import setuptools
# from setuptools_scm import get_version
setup(
    name="core_base",
    packages=find_packages(exclude=['sobase']),
    # version=get_version(),
    version="1.0.6",
    author="cx",
    author_email="2256807897@qq.com",
    description="处理Django Rbac权限,日志等",
    long_description="",
    long_description_content_type="text/markdown",
    url="http://congxing.wang",
    project_urls={
        "Bug Tracker": "http://congxing.wang",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "Django >= 4.2.0",  # Replace "X.Y" as appropriate
        "Pillow >= 9.4.0",
        "django-cors-headers >= 3.11.0",
        "django-filter >= 21.1",
        "djangorestframework >= 3.14.0",
        "djangorestframework-simplejwt >= 5.2.2",
        "requests >= 2.28.1",
        "six >= 1.16.0",
        "user-agents >= 2.2.0",
        "django-restql >= 0.15.2",
        "openpyxl >= 3.0.10",
        "pypinyin >= 0.47.1",
        "django-simple-captcha >= 0.4",
        "django-timezone-field >= 1.0",
        "pandas>=1.1.3",
        "pycryptodome>=3.15.0",
        "django-celery-beat>=2.5.0",
        "django-celery-results >=2.5.1",
        "django-comment-migrate >=0.1.7",
        "django-simple-captcha >= 0.5.17",
        "channels >= 3.0.5",
        "channels-redis >= 3.4.1",
        "mysqlclient >= 2.2.0",
        "safety >= 2.3.5"
    ]
)
