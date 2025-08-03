from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="email-header-analyzer",
    version="1.0.0",
    author="Your Name",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.39,<2.0",
        "pandas>=2.3,<3.0",
        "dnspython>=2.7,<3.0",
        "email-validator>=2.2,<3.0",
        "ipwhois>=1.3,<2.0",
        "requests>=2.32,<3.0",
        "rich>=14.1,<15.0",
        "python-dotenv>=1.1,<2.0",
        "pydantic>=2.11,<3.0",
        "plotly>=6.2,<7.0",
    ],
    entry_points={
        "console_scripts": [
            "email-header-analyzer=email_header_analyzer.main:main"
        ]
    },
)
