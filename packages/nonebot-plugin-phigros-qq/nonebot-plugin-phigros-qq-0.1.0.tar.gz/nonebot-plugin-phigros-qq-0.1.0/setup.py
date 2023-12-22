from setuptools import setup

setup(
    name="nonebot-plugin-phigros-qq",
    version="0.1.0",
    packages=["nonebot_plugin_phigros_qq"],
    install_requires=["nonebot2","Pillow","httpx","pathlib","uuid","nonebot-adapter-qq"],
    package_data={
        '': ['simyou.ttf'],
    },
    description="一个简单的基于PhigrosLibrary的Phigros查分插件，适用于nonebot-adapter-qq",
    author="NightWind",
    author_email="2125714976@qq.com",
    url="https://github.com/XTxiaoting14332/nonebot-plugin-phigros-qq",
)
