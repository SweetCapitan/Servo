"""Small wrapper over PyMongo for easy acces to bot settings/paramets """

import asyncio
import logger
import string
import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017")
collection = myClient["servoDb"]["settings"]

"""Initialization for first start. Writes primary settings in db"""
async def initialize():
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

"""Set specific parameter into document"""
async def set(name: string, value: string):
    mydick = { "settingName": name, "settingValue": value}
    collection.insert_one(mydick)
    logger.log(f"Добавленн параметр {mydick}")

"""Set two or more parameters in document"""
async def setMany(paramDict: dict):
    collection.insert_many(paramDict)
    logger.log(f"Добавленн массив параметров {paramDict}")


"""No matter how strange, this function responsible to get parameter value"""
async def get(name: string):
    return collection.find_one({"settingName": name})

"""Of corse this is update function"""
async def update(name: string, value: string):
    collection.update_one({"settingName": name}, {"$set": { "settingValue": value}})
    logger.log("Обговнен параметр %s" % {'settingName': name, 'settingValue': value})

"""HACK ALL PENTAGON BASES"""
def delete(name: string):
    collection.delete_one({"settingName": name})
    print(f"Удален параметр {name}")