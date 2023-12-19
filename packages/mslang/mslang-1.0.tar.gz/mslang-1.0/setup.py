from setuptools import setup, find_packages

setup(
    name="mslang",
    version="1.0",
    license='MIT',
    author="Sejinjin",
    author_email="sejinjin1101@gmail.com",
    description="it's very hard code",
    long_description=open('README.md').read(),
    url="https://github.com/sejin0104/morse_code",
    packages=find_packages(exclude=[]),
    keywords=['sejinjin','language','funny'],
    zip_safe=False,
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)