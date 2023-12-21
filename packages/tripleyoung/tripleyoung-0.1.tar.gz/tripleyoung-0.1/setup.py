from setuptools import setup, find_packages

setup(
    name='tripleyoung',
    version='0.1',
    packages=find_packages(),
    description='A simple Python library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/dudnjsckrgo/tripleyoung',
    license='LICENSE',
    install_requires=[
        # 필요한 의존성 패키지 나열
    ],
    classifiers=[
        # PyPI 분류자
        # 참조: https://pypi.org/classifiers/
    ],
)
