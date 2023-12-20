"""
setup.py

打包命令：
python setup.py sdist bdist_wheel
pip install dist/你的包名-版本号-py3-none-any.whl

"""
from setuptools import setup, find_packages

setup(
    name='dataeng_sdk',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            # 如果需要可以添加脚本入口点, 例如:
            # 'script-name = mypackage.module:function'
        ],
    },
    # 其它关于包的信息
    author='qiguoning01',
    author_email='qiguoning01@baidu.com',
    description='dataengine 平台算子接入sdk',
    long_description=open('README.md', encoding='utf-8').read(),
    url='https://console.cloud.baidu-int.com/devops/icode/repos/baidu/dataeng/dataeng-sdk/tree/master',
    # ...
)