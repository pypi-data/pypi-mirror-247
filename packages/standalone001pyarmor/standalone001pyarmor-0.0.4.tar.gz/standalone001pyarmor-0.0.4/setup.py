

from setuptools import setup, find_packages

setup(
    name='standalone001pyarmor',
    version='0.0.4',
    packages=find_packages(),
    description='一个 Python 混淆工具包',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='您的名字',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/standalone001pyarmor',
    install_requires=open('requirements.txt').read().splitlines(),
    package_data={
        # 包含 core 目录下的 pytransform 文件
         'standalone001pyarmor': ['core/*', 'dist/*', 'core/pytransform/*'],


        # 如果有其他需要包含的文件，例如混淆后的代码和测试文件
        # 'standalone001pyarmor.core': ['exfn001add.py', 'test_fn001add.py'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

