import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jtrends",
    version="0.0.1",
    author="takahiro ishii",
    author_email="ishii.takahiro.761@outlook.jp",
    description="This Python script fetches Google Trends data for specific keywords over the past 7 days in Japan and plots the relative interest over time, handling rate limits by pausing for 60 seconds if necessary.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ishishishi/jtrends",
    project_urls={
        "Bug Tracker": "https://github.com/ishishishi/jtrends",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['jtrends'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.11",
    entry_points = {
        'console_scripts': [
            'jtrends = jtrends:main'
        ]
    },
)
