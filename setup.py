# vim: set fileencoding=utf-8 :

import setuptools

setuptools.setup(
        name="s3etag",
        version="0.1.2",
        description="Compute AWS S3 Etags.",
        author="LiosK",
        author_email="contact@mail.liosk.net",
        url="https://github.com/LiosK/s3etag",
        packages=setuptools.find_packages(),
        entry_points={
            "console_scripts": ["s3etag=s3etag:main"],
            },
        classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3 :: Only",
            ],
        )
