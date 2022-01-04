import json
from os import name

from database.database import Database
from objects.asset import Asset
from objects.assetManager import AssetManager
from objects.prop import Prop
from objects.tile import Tile


def setup():
    print("Are you sure you want to do this?")
    print("!!! Existing tables will be dropped !!!")
    print("(Enter) continue")
    print("(Ctrl-C) to stop", end="")

    input()

    print("Creating tables:")
    createTables()

    print("Populating tables:")
    populateAssets()


def createTables():
    database = Database()
    print("--Droping existing tables")
    database.execute(Asset.SqlDropTable())

    print("--Creating new tables")
    database.execute(Asset.SqlCreateTable())
    database.close()


def populateAssets():

    database = Database()

    jsonFile = open('etc/index.json')
    objects = json.load(jsonFile)
    jsonFile.close()

    sqlQuerry = ""

    print("--Generating Tile SQL: ")
    for pos, object in enumerate(objects["Tiles"]):
        tile = Tile(AssetManager.remap(object))
        sqlQuerry += tile.SqlValues()

    print("--Generating Prop SQL: ")
    for pos, object in enumerate(objects["Props"]):
        prop = Prop(AssetManager.remap(object))
        sqlQuerry += prop.SqlValues()

    print("--Executing SQL ( takes ~3 min ) ")
    database.executeScript(sqlQuerry)
    database.close()
