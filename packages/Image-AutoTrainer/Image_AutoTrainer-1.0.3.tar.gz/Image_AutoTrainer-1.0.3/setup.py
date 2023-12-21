from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
name="Image_AutoTrainer",
version='1.0.3',
packages=find_packages(),
include_package_data=True,
license='MIT',
  description = "It's an auto image classification library",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/yinsights8/Image_AutoTrainer",
  author = 'Yash Dhakade',
  author_email = 'yinsights8@gmail.com',
  keywords = ['autotrainer'],
  install_requires=[
        'tensorflow==2.15.0',
        'scipy==1.11.4',
        'numpy==1.26.2',
        'pandas',
        'Pillow==10.1.0',
        'Flask==3.0.0',
        'Flask-Cors==3.0.10'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',

  ],
  entry_points={
        "console_scripts": [
            "autotrainer = Image_AutoTrainer.app:start_app",
        ]},
)