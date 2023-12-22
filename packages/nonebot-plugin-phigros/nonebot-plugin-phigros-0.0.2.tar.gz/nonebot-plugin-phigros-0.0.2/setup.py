from setuptools import setup

setup(
    name="nonebot-plugin-phigros",
    version="0.0.2",
    packages=["nonebot_plugin_phigros"],
    install_requires=["nonebot2","Pillow","httpx","sqlite3","pathlib","uuid","nonebot_plugin_session"],
    package_data={
        '': ['simyou.ttf'],
    },
    description="一个简单的基于PhigrosLibrary的Phigros查分插件，适用于Nonebot2",
    author="NightWind",
    author_email="2125714976@qq.com",
    url="https://github.com/XTxiaoting14332/nonebot-plugin-phigros",
)
