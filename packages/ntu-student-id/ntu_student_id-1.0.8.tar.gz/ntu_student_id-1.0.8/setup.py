from setuptools import setup, find_packages

setup(
    name="ntu_student_id",
    version="1.0.8",
    author="Max Yi-Hsun Chou",
    author_email="maxchou415@gmail.com",
    description="Get department information by NTU student ID",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/maxchou415/ntu_student_id.py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_data={
        "ntu_student_id": ["ntu_student_id/data/departments.json"],
    },
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.7",
)
