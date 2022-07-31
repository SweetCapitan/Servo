"""Small wrapper over PyMongo for easy acces to bot settings/paramets """

import asyncio
from Utilities import logger
import string
import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017")
collection = myClient["servoDb"]["settings"]

async def initialize():
    """Initialization for first start. Writes primary settings in db"""
    collist = myClient["servoDb"].list_collection_names()
    if "settings" in collist:
        logger.log("БД уже существует. Пропускаю её заполнение.")
        return

    botSettings = [
        {'name': 'covid_time', 'value': 1643703600},
        {'name': 'streaming_status_text', 'value': 'MONGODB-POWER!'},
        {'name': 'role_rainbow', 'value': 'Rainbow'},
        {'name': 'role_rainbow_status', 'value': True},
        {'name': 'kgb_mode', 'value': False}
    ]
                
    await setMany(botSettings)

async def set(name: string, value: string):
    """Async set specific parameter into document"""
    mydick = { "settingName": name, "settingValue": value}
    collection.insert_one(mydick)
    logger.log(f"Добавленн параметр {mydick}")

async def setMany(paramDict: dict):
    """Set two or more parameters in document"""
    collection.insert_many(paramDict)
    logger.log(f"Добавленн массив параметров {paramDict}")


async def get(name: string):
    """No matter how strange, this function responsible to async get parameter value"""
    return collection.find_one({"settingName": name})

def notAsyncGet(name: string):
    """No matter how strange, this function responsible to simple get parameter value"""
    return collection.find_one({"settingName": name})

async def update(name: string, value: string):
    """Of corse this is update function"""
    collection.update_one({"settingName": name}, {"$set": { "settingValue": value}})
    logger.log("Обговнен параметр %s" % {'settingName': name, 'settingValue': value})

def delete(name: string):
    """HACK ALL PENTAGON BASES"""
    collection.delete_one({"settingName": name})
    print(f"Удален параметр {name}")