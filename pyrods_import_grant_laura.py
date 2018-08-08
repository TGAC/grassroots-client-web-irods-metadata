#!env python
import os, sys, argparse, pprint, json, shlex, subprocess
from irods.session import iRODSSession
from irods.models import Collection, DataObject, DataAccess, User

# if a dir is specified, parse only that dir
parser = argparse.ArgumentParser(description='Process reads dir')
parser.add_argument('--indir', type=str, default="", help='Process this dir only')
args = parser.parse_args()
indir = args.indir

# remove any pre-existing metadata
removeMetadata = False

# skip any directories that have previously been processed and validated
skipValid = False

# output depth
verbose = True
veryverbose = True

# grassroots-3

# 964c74e8-3aba-4b1c-ae2e-4d02e3ada7bd - wuff

# 23d7d677-52fa-452e-ba7e-9d1a3a5f0c02 - laura

# 37e03dce-30c8-4e98-b76c-7d0c53d4896d - bernardo

# b0f20e9f-23f6-4cd3-bfd3-3910a1d472e8 - toronto index page

# grassroots-4
#
# 9791ca43-ddf0-4bfe-8fc0-50ff69cd6229  - wuff
#
# ffc3e90f-7f89-4934-8e35-943bb64d1789  - laura
#
# b72884b3-5e52-4032-82d7-c0a3da40d171 - bernardo
#
# 5bb7cdc1-ddb0-4354-b74a-51a78f678341 - toronto index page

# 3f00675f-836c-4364-9210-71794d8ff26e - ricardo


pp = pprint.PrettyPrinter(indent=4)


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True

ricardoUUID = "3f00675f-836c-4364-9210-71794d8ff26e"
wuffprojectUUID = "9791ca43-ddf0-4bfe-8fc0-50ff69cd6229"
lauraprojectUUID = "ffc3e90f-7f89-4934-8e35-943bb64d1789"
bernardoprojectUUID = "b72884b3-5e52-4032-82d7-c0a3da40d171"
projectUUID = wuffprojectUUID

g1 = "BB/N005104/1"
g2 = "BB/N005155/1"
g3 = "BB/L011786/1"
g4 = "BB/N020871/1"
g5 = "BB/P016855/1"

sess = iRODSSession(host='localhost', port=1247, user='rods', password='rods', zone='grassrootsZone')
coll = sess.collections.get("/grassrootsZone/public/under_license/toronto/Gardiner_2018-01-29_Watkins-diversity-12Mb")

coll.metadata.add("Project Code", g1)
coll.metadata.add("Project Code", g2)
coll.metadata.add("Project Code", g3)
coll.metadata.add("Project Code", g4)
coll.metadata.add("Project Code", g5)

for collection, subcollections, data_objects in coll.walk(topdown=True):

    if (len(data_objects) > 0):
        for dobj in data_objects:

            dobj.metadata.add("Project Code", g1)
            dobj.metadata.add("Project Code", g2)
            dobj.metadata.add("Project Code", g3)
            dobj.metadata.add("Project Code", g4)
            dobj.metadata.add("Project Code", g5)
            if (veryverbose): print(dobj.metadata.items())


    if (len(subcollections) > 0):
        for subc in subcollections:

            subc.metadata.add("Project Code", g1)
            subc.metadata.add("Project Code", g2)
            subc.metadata.add("Project Code", g3)
            subc.metadata.add("Project Code", g4)
            subc.metadata.add("Project Code", g5)
            if (veryverbose): print(subc.metadata.items())

