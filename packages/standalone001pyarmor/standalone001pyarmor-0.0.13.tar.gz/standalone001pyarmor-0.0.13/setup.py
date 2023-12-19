

from setuptools import setup, find_packages

setup(
    name='standalone001pyarmor',
    version='0.0.13',
    packages=find_packages(),
    package_data={
        # 包含 core 目录下的 pytransform 文件
         'standalone001pyarmor': [
         'core/*', 
         'dist/*', 
         'dist/test_fn001add_dist.py',
         'core/exfn001add.py',
         'dist/pytransform/*'],
        # 如果有其他需要包含的文件，例如混淆后的代码和测试文件
        # 'standalone001pyarmor.core': ['exfn001add.py', 'test_fn001add.py'],
    },
    description='一个 Python 混淆工具包',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='xiaowen',
    author_email='xiaowenseekjob@gmail.com',
    url='https://github.com/yourusername/standalone001pyarmor',
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

