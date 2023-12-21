from setuptools import setup, find_packages

setup(
    name='nonebot-plugin-phigros-qq',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        'Pillow','nonebot2'
    ],
    package_data={
        '': ['simyou.ttf'],
    },
    author='NightWind',
    author_email='2125714976@qq.com',
    description='一个简单的基于PhigrosLibrary的Nonebot Phigros查分插件，适用于Adapter-qq',
    url='https://github.com/XTxiaoting14332/nonebot-plugin-phigros-qq',
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
)
