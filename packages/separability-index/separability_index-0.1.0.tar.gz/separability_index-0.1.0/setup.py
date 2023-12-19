from setuptools import setup, find_packages, Extension

with open("README.md","r", encoding = 'utf-8') as fp:
	readme = fp.read()

setup(
	name="separability_index",
	version="0.1.0",
	description="A suite of tools to assess the separability of two datasets.",
	author="A. Renmin Pretell Ductram, Scott J. Brandenberg",
	author_email="rpretell@unr.edu, sjbrandenberg@ucla.edu",
	url="https://github.com/RPretellD/separability_index",
    long_description=readme,
    
    packages=find_packages(),
	include_package_data=True,
	
    install_requires=["numpy"],

	license="MIT",
	keywords="separability",
	classifiers=[
        "Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	]
)