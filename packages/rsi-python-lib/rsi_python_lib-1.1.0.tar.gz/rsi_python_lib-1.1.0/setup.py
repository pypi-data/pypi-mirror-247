from distutils.core import setup

setup(
    name="rsi_python_lib",
    packages=["rsi_python_lib"],
    version="1.1.0",
    license="MIT",
    description="A simple Python library for the RSI services ",
    author = "Claudio Perucca",
    author_email = "claudio.perucca@rsi.ch",
    download_url = "https://github.com/peruccac/Rsi_python_lib/archive/refs/tags/1.0.0.tar.gz", 
    install_requires=[ 
          'requests',
          'python-dateutil',
          'boto3'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
