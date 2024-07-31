import logging

import aiohttp


from config import LoraApiConfig

api_config = LoraApiConfig()


async def get_device_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{api_config.api_uri}/api/v1/devices/") as response:
            data = await response.json()
            return [device["device"] for device in data]


async def get_tilt_data(dev_eui: str, from_timestamp: int, to_timestamp: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{api_config.api_uri}/api/v1/tilt/?dev_eui={dev_eui}&from_timestamp={from_timestamp}&to_timestamp={to_timestamp}"
        ) as response:
            data = await response.json()
            return data["data"]


async def get_last_tilt_data(dev_eui: str, from_timestamp: int, to_timestamp: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{api_config.api_uri}/api/v1/tilt/?dev_eui={dev_eui}&from_timestamp={from_timestamp}&to_timestamp={to_timestamp}"
        ) as response:
            data = await response.json()
            return data["data"][-1]
