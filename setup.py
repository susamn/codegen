import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    setuptools.setup(
        name="codegen",
        version="0.0.1",
        author="Supratim Samanta",
        author_email="tech.supratim.samanta@gmail.com",
        description="A helper package to generate code from declarative json",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/susamn/codegen",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: MIT",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
    )
