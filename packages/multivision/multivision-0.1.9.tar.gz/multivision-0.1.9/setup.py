import setuptools
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multivision",
    version="0.1.9",
    license='MIT',
    author="Falahgs.G.Saleih",
    author_email="falahgs07@gmail.com",
    description="Create Object Segmentation Labels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/falahgs/",
    packages=find_packages(),
    keywords=['transformers', 'datasets'],
    install_requires=['autodistill_yolov8','autodistill_grounding_dino','reportlab', 'ultralytics', 'Pillow', 'roboflow', 'autodistill-grounded-sam==0.1.1',
                      'google-images-downloader==1.0.16', 'pytube'],
    classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent", ],
    python_requires='>=3.6',
    #package_data={'multivision': ['data/*', 'multivision/*']
    #}
)
