#!env python
import os, sys, argparse, pprint, json, shlex, subprocess
from irods.session import iRODSSession
from irods.models import Collection, DataObject, DataAccess, User

lispyrods = [
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "synthetic/AB/ByGene/PRJNA319131_count.tsv",
        "short_description": "Raw counts for the tetraploid samples by gene"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "synthetic/AB/ByGene/PRJNA319131_tpm.tsv",
        "short_description": "Raw TPMs for the tetraploid samples by gene"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/AB/ByTranscript/PRJNA319131_count.tsv",
        "short_description": "Raw counts for the tetraploid samples by transcript"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/AB/ByTranscript/PRJNA319131_tpm.tsv",
        "short_description": "Raw TPMs for the tetraploid samples by transcript"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/AB/PRJNA319131_summary.tsv",
        "short_description": "Mapping summary for the tetraploid samples"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/ABD/ByGene/PRJNA319131_count.tsv",
        "short_description": "Raw counts for the hexaploid samples by gene"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/ABD/ByGene/PRJNA319131_tpm.tsv",
        "short_description": "Raw TPMs for the hexaploid samples by gene"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/ABD/ByTranscript/PRJNA319131_count.tsv",
        "short_description": "Raw counts for the hexaploid samples by transcript"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/ABD/ByTranscript/PRJNA319131_tpm.tsv",
        "short_description": "Raw TPMs for the hexaploid samples by transcript"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/ABD/PRJNA319131_summary.tsv",
        "short_description": "Mapping summary for the hexaploid samples"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/D/ByGene/PRJNA319131_count.tsv",
        "short_description": "Raw counts for the diploid samples by gene"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/D/ByGene/PRJNA319131_tpm.tsv",
        "short_description": "Raw TPMs for the diploid samples by gene"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/D/ByTranscript/PRJNA319131_count.tsv",
        "short_description": "Raw counts for the diploid samples by transcript"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/D/ByTranscript/PRJNA319131_tpm.tsv",
        "short_description": "Raw TPMs for the diploid samples by transcript"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/D/PRJNA319131_summary.tsv",
        "short_description": "Mapping summary for the diploid samples"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/LeafCategories_hc_Development_no_stress.csv",
        "short_description": "Expression bias categories for the genes in the HC_Development set for the leaf samples (use as baseline)"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/MinTPM1_LeafCategories_hc_cs_no_stress.csv",
        "short_description": "Expression bias categories for the synteic leaf samples"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/metadata_ABD_synthetic.txt",
        "short_description": "Metadata the hexaploid synthetic hybrids"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/metadata_AB_synthetic.txt",
        "short_description": "Metadata for the tetraploid progenitors"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/metadata_D_synthetic.txt",
        "short_description": "Metadata for the diploid progenitors"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        
        "file": "synthetic/mini_metadata.txt",
        "short_description": "Metadata for all the samples in PRJNA319131"
    }
]


sess = iRODSSession(host='localhost', port=1247, user='rods', password='', zone='grassrootsZone')


for ob in lispyrods:
    dobj = sess.data_objects.get('/grassrootsZone/public/under_license/toronto/Ramirez-Gonzalez_etal_2018-06025-Transcriptome-Landscape/' + ob['file'])
    print(ob['project_name'])
    for k,v in ob.items():
        if (k != 'file'):
            dobj.metadata.add(k, v)
            print(dobj.metadata.items())
