# -*- coding: utf-8 -*-
# @author: xiao bai

from setuptools import setup, find_packages

setup(
    name='zerorunner-consul',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        "requests"
        # 任何依赖项都在这里列出
    ],
    extras_require={
        'asyncio': ['aiohttp'],
    },
    author='xiao.bai',
    author_email='546142369@qq.com',
    description='Python client for Consul (https://www.consul.io/)',
    license='MIT',
    keywords='',
    url='https://github.com/baizunxian/zerorunner-consul'
)
