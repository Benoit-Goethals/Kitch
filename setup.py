from setuptools import setup, find_packages

setup(
    name="Kitch",  # Project name
    version="0.1.0",  # Initial version
    packages=find_packages(exclude=["tests", "tests.*"]),  # Automatically find all packages
    install_requires=[
        "click",
        "flask",
        "jinja2",
        "matplotlib",
        "numpy",
        "pandas",
        "pillow",
        "plotly",
        "pyparsing",
        "pytz",
        "pyyaml",
        "redis",
        "requests",
        "seaborn",
        "sqlalchemy",
        "werkzeug",
        "asyncpg",
        "shiny",
    ],
    extras_require={
        'dev': [
            'pytest',
            'ipython',
        ],
    },
    python_requires=">=3.8",  # Minimum required Python version
    author="Your Name",  # Replace with your name
    author_email="your.email@example.com",  # Replace with your contact email
    description="A web-based data visualization and management tool for projects and tasks",
    long_description=open("README.md").read(),  # Include content from README.md
    long_description_content_type="text/markdown",  # Specify content type
    url="https://github.com/yourusername/kitch",  # Replace with project URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "kitch-app=app:shiny_app",  # Make the app executable as 'kitch-app'
        ],
    },
    include_package_data=True,  # Include non-code files from MANIFEST.in
    package_data={
        # Include configuration files or other resources
        "": ["*.yaml", "*.yml", "*.json", "*.html", "*.css", "*.js"],
    },
    license="MIT",  # Replace with actual license
)