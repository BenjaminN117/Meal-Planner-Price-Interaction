from setuptools import find_packages, setup
setup(
    name='NotionAPI',
    packages=find_packages(include=['NotionAPI']),
    version='0.1.2',
    description='Notion API interactions',
    author='Benjamin Norman',
    license='MIT',
    install_requires=["requests"],
    setup_requires=['pytest-runner'],
)