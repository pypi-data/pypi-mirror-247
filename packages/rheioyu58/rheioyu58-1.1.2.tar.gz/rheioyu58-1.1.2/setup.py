from setuptools import setup, find_packages
from pkg_resources import parse_requirements
import pathlib

DISTNAME = 'rheioyu58'
DESCRIPTION = ''
MAINTAINER = 'AxcelerateAI'
MAINTAINER_EMAIL = 'rmznmqsd2@gmail.com'
URL = 'https://github.com/augmentedstartups/AS-One.git'
DOWNLOAD_URL = URL

VERSION = '1.1.2'

with open('README.md') as f:
    long_description = f.read()

requirements_txt = pathlib.Path('requirements.txt').open()


def setup_package():
    setup(
        name=DISTNAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description = long_description,
        long_description_content_type='text/markdown',
        url=DOWNLOAD_URL,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        license='BSD 2-clause',
        keywords=' inferencing',
        # package_dir={"":""},
        packages=find_packages(),
        setup_requires=['numpy', 'Cython', 'cython-bbox'],
        dependency_links=[
            "https://download.pytorch.org/whl/cu113/",
            'https://pypi.python.org/simple/'],
        install_requires=[str(requirement)
                          for requirement in parse_requirements(requirements_txt)],
        
        extras_require={
            'extras': [
                'onnxruntime-gpu==1.12.1',
                'typing_extensions==4.4.0',
                'super-gradients==3.1.1',
                'pillow==9.5.0'
            ]
        },
        data_files=[('', ['requirements.txt'])],  #
        package_data={
            "": ["detectors/yolor/cfg/*.cfg", "detectors/data/*.yaml",
                         "detectors/data/*.yml", "detectors/data/*.names"],
        },

        include_package_data=True,
        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows :: Windows 10',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
        ],
    )


if __name__ == "__main__":
    setup_package()
