import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
        name='DRMAAtic-lib',
        version='1.0.7',
        author='Alessio Del Conte',
        author_email='alessio.delconte@phd.unipd.it',
        description='DRMAA interface for Slurm/SGE DRMs @ BioComputingUP lab',
        long_description=long_description,
        long_description_content_type="text/markdown",
        license='MIT',
        packages=setuptools.find_packages(),
        install_requires=['drmaa'],
        python_requires='>=3.6',
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Unix",
        ],
)
