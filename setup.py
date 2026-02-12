"""
NetOpsForge - Network Operations Automation Platform
Setup configuration
"""

from setuptools import setup, find_packages
import sys

# Platform-specific dependencies
install_requires = [
    "pyyaml>=6.0.1",
    "click>=8.1.7",
    "colorama>=0.4.6",
    "python-dotenv>=1.0.0",
    "netmiko>=4.3.0",
    "textfsm>=1.1.3",
    "napalm>=4.1.0",
    "requests>=2.31.0",
    "linear-sdk>=2.0.0",
    "jinja2>=3.1.3",
    "tabulate>=0.9.0",
    "pandas>=2.2.0",
    "structlog>=24.1.0",
]

# Add Windows-specific dependencies
if sys.platform == "win32":
    install_requires.append("pywin32>=306")

setup(
    name="netopsforge",
    version="0.1.0",
    description="Network Operations Automation Platform with AI Integration",
    author="Jesse Tucker",
    author_email="jesse.tucker@bldr.com",
    url="https://github.com/JT-BFS/NetOpsForge",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "netopsforge=netopsforge.cli:main",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

