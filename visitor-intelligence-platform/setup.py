from setuptools import find_packages, setup

setup(
    name="visitor-intelligence-platform",
    version="0.1.0",
    description="Synthetic FIFA 2026 visitor data generator",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["faker==24.2.0"],
    python_requires=">=3.10",
)
