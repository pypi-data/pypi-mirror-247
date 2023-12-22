import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covidbeta",
    version="0.0.1",
    author="Yugo Ishihara",
    author_email="s2022041@stu.musashino-u.ac.jp",
    description="A package for visualize expected number of new infections and new deaths by country due to Covid-19.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yugo-Ishihara/covidcasev",
    project_urls={
        "covidbeta": "https://github.com/yugo-Ishihara/covidcasev",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['covidbeta'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'covidbeta = covidbeta:main'
        ]
    },
)
