#!env python
import os, sys, argparse, pprint, json, shlex, subprocess
from irods.session import iRODSSession
from irods.models import Collection, DataObject, DataAccess, User

lispyrods = [
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/compara_homolgy.txt",
        "short_description": "Homology obtained from Ensembl compara for IWGSC2.26"
    }
]


sess = iRODSSession(host='localhost', port=1247, user='rods', password='rods', zone='grassrootsZone')


for ob in lispyrods:
    dobj = sess.data_objects.get('/grassrootsZone/public/under_license/toronto/Ramirez-Gonzalez_etal_2018-06025-Transcriptome-Landscape/' + ob['File'])
    print(ob['project_name'])
    for k,v in ob.items():
        if (k != 'file'):
            dobj.metadata.add(k, v)
            print(dobj.metadata.items())
