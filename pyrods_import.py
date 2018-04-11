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

# 964c74e8-3aba-4b1c-ae2e-4d02e3ada7bd - wuff

# 23d7d677-52fa-452e-ba7e-9d1a3a5f0c02 - laura

# 37e03dce-30c8-4e98-b76c-7d0c53d4896d - bernardo

# b0f20e9f-23f6-4cd3-bfd3-3910a1d472e8 - toronto index page

pp = pprint.PrettyPrinter(indent=4)


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True


projectUUID = "964c74e8-3aba-4b1c-ae2e-4d02e3ada7bd"

sess = iRODSSession(host='localhost', port=1247, user='rods', password='rods', zone='grassrootsZone')
coll = sess.collections.get("/grassrootsZone/public/under_license/toronto/Wulff_2018-01-31_OWWC")

coll.metadata.add("project_uuid", projectUUID)

for collection, subcollections, data_objects in coll.walk(topdown=True):

    if (len(data_objects) > 0):
        for dobj in data_objects:

            dobj.metadata.add("project_uuid", projectUUID)
            if (veryverbose): print(dobj.metadata.items())


    if (len(subcollections) > 0):
        for subc in subcollections:

            subc.metadata.add("project_uuid", projectUUID)
            if (veryverbose): print(subc.metadata.items())

