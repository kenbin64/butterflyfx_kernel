"""
ButterflyFX Kernel - Dimensional Computing Foundation
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="butterflyfx-kernel",
    version="1.0.0",
    author="Kenneth Bingham",
    author_email="keneticsart@gmail.com",
    description="Dimensional Computing Foundation - A 7-level helix model replacing tree-based hierarchical structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kenbin64/butterflyfx_kernel",
    project_urls={
        "Bug Tracker": "https://github.com/kenbin64/butterflyfx_kernel/issues",
        "Documentation": "https://butterflyfx.us",
        "Source Code": "https://github.com/kenbin64/butterflyfx_kernel",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",  # CC BY 4.0 compatible
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ],
        "server": [
            "aiohttp>=3.8.0",
            "websockets>=11.0.0",
        ],
        "audio": [
            "sounddevice>=0.4.6",
        ],
    },
    keywords=[
        "dimensional-computing",
        "helix",
        "mathematical-kernel",
        "state-machine",
        "paradigm",
        "manifold",
        "substrate",
        "golden-ratio",
        "fibonacci",
    ],
)
