import logging
import pymongo
from bson.objectid import ObjectId
from django.conf import settings

try:
    DEV_DB = pymongo.MongoClient(settings.DEV_API_DB)[settings.DEV_API_DB_NAME]
    DEV_DB.authenticate(settings.DEV_API_DB_USER,settings.DEV_API_DB_PASS)
    DEV_API_GROUPS=[]

    def loadDevApiGroups():
        global DEV_API_GROUPS
        DEV_API_GROUPS=[]
        parents=DEV_DB["groups"].find({"$and":[{"$or":[{"parentId":{"$type":10}},{"parentId":{"$exists":False}}]},{"isDeleted":False}]})
        # print(parents.count())
        def getGroupInfo(parent):
            groupInfo={"id":str(parent["_id"]),"label":parent["name"]}
            childs=DEV_DB["groups"].find({"parentId":parent["_id"],"isDeleted":False})
            if childs.count()>0:
                groupInfo["children"]=[]
                for child in childs:
                    groupInfo["children"].append(getGroupInfo(child))
            return groupInfo

        for parent in parents:
            # print("%s,%s,%s" % (parent["_id"],parent["name"],parent["parentId"] if "parentId" in parent else None))
            groupInfo=getGroupInfo(parent)
            DEV_API_GROUPS.append(groupInfo)
        # print(DEV_API_GROUPS)
    loadDevApiGroups()
except:
    pass

def getDevApiGroups():
    return DEV_API_GROUPS

def getChildGroups(group):
    groupId=ObjectId(group)
    groups=[]
    groups.append(groupId)
    childs=DEV_DB["groups"].find({"parentId":groupId,"isDeleted":False})
    if childs.count()>0:
        for child in childs:
            groups.extend(getChildGroups(child["_id"]))
    return groups

def getDevApis(groupId):
    return DEV_DB["apis"].find({"group":groupId,"isDeleted":False})