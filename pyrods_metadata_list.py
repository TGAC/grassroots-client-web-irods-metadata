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
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/Triticum_aestivum.IWGSC2.26.cdna.all.fa.gz",
        "short_description": "Transcriptome reference IWGSC2.26"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/HC_triads_for_expvip.tab",
        "short_description": "Homology triads described in https://dx.doi.org/10.1126/science.aar7191"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/IWGSCv1.0_UTR_ALL.cdnas.fasta.gz",
        "short_description": "Transcriptome reference described in http://dx.doi. org/10.1126/ science.aar6089"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/IWGSC_v1.1_ALL_20170706_transcripts.fasta.gz",
        "short_description": "Transcriptome reference described in https://dx.doi.org/10.1126/science.aar7191"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/compara_homolgy_32_85.txt",
        "short_description": "Homology obtained from Ensembl compara for TGACv1"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/Triticum_aestivum_CS42_TGACv1_scaffold.annotation.gff3.cdna.fa.gz",
        "short_description": "Transcriptome reference described in https://dx.doi.org/10.1101/gr.217117.116"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "default_metadata.txt",
        "file": "expvip/default_metadata.txt",
        "short_description": "Metadata used to populate the expVIP database"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "factor_order.txt",
        "file": "expvip/factor_order.txt",
        "short_description": "Default order to display the factors in expVIP"
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/developing spike_summary.tsv",
        "short_description": "Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/PAMP Triggered Imune Response_summary.tsv",
        "short_description": "Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26_summary.txt",
        "file": "expvip/IWGSC2.26_summary.txt",
        "short_description": "Summary of number of reads and mapped reads to the IWGSC2.26_summary.txt  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/developing spike_summary.tsv",
        "short_description": "Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/PAMP Triggered Imune Response_summary.tsv",
        "short_description": "Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0_summary.txt",
        "file": "expvip/RefSeq_1.0_summary.txt",
        "short_description": "Summary of number of reads and mapped reads to the RefSeq_1.0_summary.txt  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/developing spike_summary.tsv",
        "short_description": "Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/PAMP Triggered Imune Response_summary.tsv",
        "short_description": "Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1_summary.txt",
        "file": "expvip/RefSeq_1.1_summary.txt",
        "short_description": "Summary of number of reads and mapped reads to the RefSeq_1.1_summary.txt  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/developing spike_summary.tsv",
        "short_description": "Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/PAMP Triggered Imune Response_summary.tsv",
        "short_description": "Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1_summary.txt",
        "file": "expvip/TGACv1_summary.txt",
        "short_description": "Summary of number of reads and mapped reads to the TGACv1_summary.txt  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP067916_summary.tsv",
        "short_description": "Chinese Spring flag leaves, 6 timepoints   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP067916_summary.tsv",
        "short_description": "Chinese Spring flag leaves, 6 timepoints   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP067916_summary.tsv",
        "short_description": "Chinese Spring flag leaves, 6 timepoints   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP067916_summary.tsv",
        "short_description": "Chinese Spring flag leaves, 6 timepoints   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP067916_count.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP067916_count.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP067916_count.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP067916_count.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP067916_tpm.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP067916_tpm.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP067916_tpm.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP067916_tpm.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP067916_count.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP067916_count.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP067916_count.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP067916_count.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP067916_tpm.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP067916_tpm.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP067916_tpm.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP067916_tpm.tsv.gz",
        "short_description": "Chinese Spring flag leaves, 6 timepoints transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/Aneuploidy_summary.tsv",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/Aneuploidy_summary.tsv",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/Aneuploidy_summary.tsv",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/Aneuploidy_summary.tsv",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/Aneuploidy_count.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/Aneuploidy_count.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/Aneuploidy_count.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/Aneuploidy_count.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/Aneuploidy_tpm.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/Aneuploidy_tpm.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/Aneuploidy_tpm.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/Aneuploidy_tpm.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/Aneuploidy_count.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/Aneuploidy_count.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/Aneuploidy_count.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/Aneuploidy_count.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/Aneuploidy_tpm.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/Aneuploidy_tpm.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/Aneuploidy_tpm.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/Aneuploidy_tpm.tsv.gz",
        "short_description": "Chinese Spring leaves and roots from seven leaf stage transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/CS_methylome_summary.tsv",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/CS_methylome_summary.tsv",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/CS_methylome_summary.tsv",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/CS_methylome_summary.tsv",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/CS_methylome_count.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/CS_methylome_count.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/CS_methylome_count.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/CS_methylome_count.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/CS_methylome_tpm.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/CS_methylome_tpm.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/CS_methylome_tpm.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/CS_methylome_tpm.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/CS_methylome_count.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/CS_methylome_count.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/CS_methylome_count.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/CS_methylome_count.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/CS_methylome_tpm.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/CS_methylome_tpm.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/CS_methylome_tpm.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/CS_methylome_tpm.tsv.gz",
        "short_description": "Chinese Spring seedling (leaves and roots) and spikes at anthesis transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/CS_spike_summary.tsv",
        "short_description": "Chinese Spring spike timecourse   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/CS_spike_summary.tsv",
        "short_description": "Chinese Spring spike timecourse   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/CS_spike_summary.tsv",
        "short_description": "Chinese Spring spike timecourse   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/CS_spike_summary.tsv",
        "short_description": "Chinese Spring spike timecourse   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/CS_spike_count.tsv.gz",
        "short_description": "Chinese Spring spike timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/CS_spike_count.tsv.gz",
        "short_description": "Chinese Spring spike timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/CS_spike_count.tsv.gz",
        "short_description": "Chinese Spring spike timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/CS_spike_count.tsv.gz",
        "short_description": "Chinese Spring spike timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/CS_spike_tpm.tsv.gz",
        "short_description": "Chinese Spring spike timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/CS_spike_tpm.tsv.gz",
        "short_description": "Chinese Spring spike timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/CS_spike_tpm.tsv.gz",
        "short_description": "Chinese Spring spike timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/CS_spike_tpm.tsv.gz",
        "short_description": "Chinese Spring spike timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/CS_spike_count.tsv.gz",
        "short_description": "Chinese Spring spike timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/CS_spike_count.tsv.gz",
        "short_description": "Chinese Spring spike timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/CS_spike_count.tsv.gz",
        "short_description": "Chinese Spring spike timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/CS_spike_count.tsv.gz",
        "short_description": "Chinese Spring spike timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/CS_spike_tpm.tsv.gz",
        "short_description": "Chinese Spring spike timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/CS_spike_tpm.tsv.gz",
        "short_description": "Chinese Spring spike timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/CS_spike_tpm.tsv.gz",
        "short_description": "Chinese Spring spike timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/CS_spike_tpm.tsv.gz",
        "short_description": "Chinese Spring spike timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP078208_summary.tsv",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot)   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP078208_summary.tsv",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot)   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP078208_summary.tsv",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot)   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP078208_summary.tsv",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot)   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP078208_count.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP078208_count.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP078208_count.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP078208_count.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP078208_tpm.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP078208_tpm.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP078208_tpm.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP078208_tpm.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP078208_count.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP078208_count.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP078208_count.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP078208_count.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP078208_tpm.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP078208_tpm.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP078208_tpm.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP078208_tpm.tsv.gz",
        "short_description": "coleoptile infection with Fusarium pseudograminearum (crown rot) transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP038912_summary.tsv",
        "short_description": "comparison of stamen, pistil and pistilloidy expression   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP038912_summary.tsv",
        "short_description": "comparison of stamen, pistil and pistilloidy expression   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP038912_summary.tsv",
        "short_description": "comparison of stamen, pistil and pistilloidy expression   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP038912_summary.tsv",
        "short_description": "comparison of stamen, pistil and pistilloidy expression   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP038912_count.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP038912_count.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP038912_count.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP038912_count.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP038912_tpm.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP038912_tpm.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP038912_tpm.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP038912_tpm.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP038912_count.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP038912_count.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP038912_count.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP038912_count.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP038912_tpm.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP038912_tpm.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP038912_tpm.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP038912_tpm.tsv.gz",
        "short_description": "comparison of stamen, pistil and pistilloidy expression transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP060670_summary.tsv",
        "short_description": "CS spikes inoculated with fusarium head blight   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP060670_summary.tsv",
        "short_description": "CS spikes inoculated with fusarium head blight   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP060670_summary.tsv",
        "short_description": "CS spikes inoculated with fusarium head blight   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP060670_summary.tsv",
        "short_description": "CS spikes inoculated with fusarium head blight   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP060670_count.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP060670_count.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP060670_count.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP060670_count.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP060670_tpm.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP060670_tpm.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP060670_tpm.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP060670_tpm.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP060670_count.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP060670_count.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP060670_count.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP060670_count.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP060670_tpm.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP060670_tpm.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP060670_tpm.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP060670_tpm.tsv.gz",
        "short_description": "CS spikes inoculated with fusarium head blight transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/Development_summary.tsv",
        "short_description": "developmental time-course of Azhurnaya   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/Development_summary.tsv",
        "short_description": "developmental time-course of Azhurnaya   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/Development_summary.tsv",
        "short_description": "developmental time-course of Azhurnaya   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/Development_summary.tsv",
        "short_description": "developmental time-course of Azhurnaya   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/Development_count.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/Development_count.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/Development_count.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/Development_count.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/Development_tpm.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/Development_tpm.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/Development_tpm.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/Development_tpm.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/Development_count.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/Development_count.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/Development_count.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/Development_count.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/Development_tpm.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/Development_tpm.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/Development_tpm.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/Development_tpm.tsv.gz",
        "short_description": "developmental time-course of Azhurnaya transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/choulet_URGI_summary.tsv",
        "short_description": "developmental time-course of Chinese Spring   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/choulet_URGI_summary.tsv",
        "short_description": "developmental time-course of Chinese Spring   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/choulet_URGI_summary.tsv",
        "short_description": "developmental time-course of Chinese Spring   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/choulet_URGI_summary.tsv",
        "short_description": "developmental time-course of Chinese Spring   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/choulet_URGI_count.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/choulet_URGI_count.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/choulet_URGI_count.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/choulet_URGI_count.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/choulet_URGI_tpm.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/choulet_URGI_tpm.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/choulet_URGI_tpm.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/choulet_URGI_tpm.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/choulet_URGI_count.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/choulet_URGI_count.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/choulet_URGI_count.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/choulet_URGI_count.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/choulet_URGI_tpm.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/choulet_URGI_tpm.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/choulet_URGI_tpm.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/choulet_URGI_tpm.tsv.gz",
        "short_description": "developmental time-course of Chinese Spring transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP041022_summary.tsv",
        "short_description": "developmental time-course of synthetic hexaploid   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP041022_summary.tsv",
        "short_description": "developmental time-course of synthetic hexaploid   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP041022_summary.tsv",
        "short_description": "developmental time-course of synthetic hexaploid   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP041022_summary.tsv",
        "short_description": "developmental time-course of synthetic hexaploid   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP041022_count.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP041022_count.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP041022_count.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP041022_count.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP041022_tpm.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP041022_tpm.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP041022_tpm.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP041022_tpm.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP041022_count.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP041022_count.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP041022_count.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP041022_count.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP041022_tpm.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP041022_tpm.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP041022_tpm.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP041022_tpm.tsv.gz",
        "short_description": "developmental time-course of synthetic hexaploid transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP045409_summary.tsv",
        "short_description": "drought and heat stress time-course in seedlings   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP045409_summary.tsv",
        "short_description": "drought and heat stress time-course in seedlings   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP045409_summary.tsv",
        "short_description": "drought and heat stress time-course in seedlings   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP045409_summary.tsv",
        "short_description": "drought and heat stress time-course in seedlings   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP045409_count.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP045409_count.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP045409_count.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP045409_count.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP045409_tpm.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP045409_tpm.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP045409_tpm.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP045409_tpm.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP045409_count.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP045409_count.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP045409_count.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP045409_count.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP045409_tpm.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP045409_tpm.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP045409_tpm.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP045409_tpm.tsv.gz",
        "short_description": "drought and heat stress time-course in seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP004884_summary.tsv",
        "short_description": "flag leaf downregulation of GPC   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP004884_summary.tsv",
        "short_description": "flag leaf downregulation of GPC   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP004884_summary.tsv",
        "short_description": "flag leaf downregulation of GPC   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP004884_summary.tsv",
        "short_description": "flag leaf downregulation of GPC   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP004884_count.tsv.gz",
        "short_description": "flag leaf downregulation of GPC gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP004884_count.tsv.gz",
        "short_description": "flag leaf downregulation of GPC gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP004884_count.tsv.gz",
        "short_description": "flag leaf downregulation of GPC gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP004884_count.tsv.gz",
        "short_description": "flag leaf downregulation of GPC gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP004884_tpm.tsv.gz",
        "short_description": "flag leaf downregulation of GPC gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP004884_tpm.tsv.gz",
        "short_description": "flag leaf downregulation of GPC gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP004884_tpm.tsv.gz",
        "short_description": "flag leaf downregulation of GPC gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP004884_tpm.tsv.gz",
        "short_description": "flag leaf downregulation of GPC gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP004884_count.tsv.gz",
        "short_description": "flag leaf downregulation of GPC transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP004884_count.tsv.gz",
        "short_description": "flag leaf downregulation of GPC transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP004884_count.tsv.gz",
        "short_description": "flag leaf downregulation of GPC transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP004884_count.tsv.gz",
        "short_description": "flag leaf downregulation of GPC transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP004884_tpm.tsv.gz",
        "short_description": "flag leaf downregulation of GPC transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP004884_tpm.tsv.gz",
        "short_description": "flag leaf downregulation of GPC transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP004884_tpm.tsv.gz",
        "short_description": "flag leaf downregulation of GPC transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP004884_tpm.tsv.gz",
        "short_description": "flag leaf downregulation of GPC transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ERP003465_summary.tsv",
        "short_description": "fusarium head blight infected spikelets   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ERP003465_summary.tsv",
        "short_description": "fusarium head blight infected spikelets   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ERP003465_summary.tsv",
        "short_description": "fusarium head blight infected spikelets   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ERP003465_summary.tsv",
        "short_description": "fusarium head blight infected spikelets   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP003465_count.tsv.gz",
        "short_description": "fusarium head blight infected spikelets gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP003465_count.tsv.gz",
        "short_description": "fusarium head blight infected spikelets gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP003465_count.tsv.gz",
        "short_description": "fusarium head blight infected spikelets gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP003465_count.tsv.gz",
        "short_description": "fusarium head blight infected spikelets gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP003465_tpm.tsv.gz",
        "short_description": "fusarium head blight infected spikelets gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP003465_tpm.tsv.gz",
        "short_description": "fusarium head blight infected spikelets gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP003465_tpm.tsv.gz",
        "short_description": "fusarium head blight infected spikelets gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP003465_tpm.tsv.gz",
        "short_description": "fusarium head blight infected spikelets gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP003465_count.tsv.gz",
        "short_description": "fusarium head blight infected spikelets transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP003465_count.tsv.gz",
        "short_description": "fusarium head blight infected spikelets transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP003465_count.tsv.gz",
        "short_description": "fusarium head blight infected spikelets transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP003465_count.tsv.gz",
        "short_description": "fusarium head blight infected spikelets transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP003465_tpm.tsv.gz",
        "short_description": "fusarium head blight infected spikelets transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP003465_tpm.tsv.gz",
        "short_description": "fusarium head blight infected spikelets transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP003465_tpm.tsv.gz",
        "short_description": "fusarium head blight infected spikelets transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP003465_tpm.tsv.gz",
        "short_description": "fusarium head blight infected spikelets transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP056412_summary.tsv",
        "short_description": "grain developmental timecourse with 4A dormancy QTL   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP056412_summary.tsv",
        "short_description": "grain developmental timecourse with 4A dormancy QTL   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP056412_summary.tsv",
        "short_description": "grain developmental timecourse with 4A dormancy QTL   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP056412_summary.tsv",
        "short_description": "grain developmental timecourse with 4A dormancy QTL   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP056412_count.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP056412_count.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP056412_count.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP056412_count.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP056412_tpm.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP056412_tpm.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP056412_tpm.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP056412_tpm.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP056412_count.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP056412_count.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP056412_count.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP056412_count.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP056412_tpm.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP056412_tpm.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP056412_tpm.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP056412_tpm.tsv.gz",
        "short_description": "grain developmental timecourse with 4A dormancy QTL transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ERP004505_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP013449_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP029372_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ERP004505_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP013449_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP029372_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ERP004505_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP013449_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP029372_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ERP004505_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP013449_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP029372_summary.tsv",
        "short_description": "grain tissue-specific developmental timecourse   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP004505_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP013449_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP029372_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP004505_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP013449_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP029372_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP004505_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP013449_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP029372_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP004505_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP013449_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP029372_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP004505_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP013449_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP029372_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP004505_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP013449_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP029372_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP004505_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP013449_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP029372_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP004505_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP013449_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP029372_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP004505_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP013449_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP029372_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP004505_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP013449_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP029372_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP004505_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP013449_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP029372_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP004505_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP013449_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP029372_count.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP004505_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP013449_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP029372_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP004505_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP013449_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP029372_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP004505_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP013449_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP029372_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP004505_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP013449_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP029372_tpm.tsv.gz",
        "short_description": "grain tissue-specific developmental timecourse transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ERP008767_summary.tsv",
        "short_description": "grain tissue-specific expression at 12 days post anthesis   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ERP008767_summary.tsv",
        "short_description": "grain tissue-specific expression at 12 days post anthesis   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ERP008767_summary.tsv",
        "short_description": "grain tissue-specific expression at 12 days post anthesis   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ERP008767_summary.tsv",
        "short_description": "grain tissue-specific expression at 12 days post anthesis   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP008767_count.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP008767_count.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP008767_count.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP008767_count.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP008767_tpm.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP008767_tpm.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP008767_tpm.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP008767_tpm.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP008767_count.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP008767_count.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP008767_count.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP008767_count.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP008767_tpm.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP008767_tpm.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP008767_tpm.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP008767_tpm.tsv.gz",
        "short_description": "grain tissue-specific expression at 12 days post anthesis transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ERP015130_summary.tsv",
        "short_description": "leaves naturally infected with Magnaporthe oryzae   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ERP015130_summary.tsv",
        "short_description": "leaves naturally infected with Magnaporthe oryzae   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ERP015130_summary.tsv",
        "short_description": "leaves naturally infected with Magnaporthe oryzae   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ERP015130_summary.tsv",
        "short_description": "leaves naturally infected with Magnaporthe oryzae   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP015130_count.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP015130_count.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP015130_count.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP015130_count.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP015130_tpm.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP015130_tpm.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP015130_tpm.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP015130_tpm.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP015130_count.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP015130_count.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP015130_count.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP015130_count.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP015130_tpm.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP015130_tpm.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP015130_tpm.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP015130_tpm.tsv.gz",
        "short_description": "leaves naturally infected with Magnaporthe oryzae transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP064598_summary.tsv",
        "short_description": "microspores in tissue culture and cold   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP064598_summary.tsv",
        "short_description": "microspores in tissue culture and cold   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP064598_summary.tsv",
        "short_description": "microspores in tissue culture and cold   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP064598_summary.tsv",
        "short_description": "microspores in tissue culture and cold   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP064598_count.tsv.gz",
        "short_description": "microspores in tissue culture and cold gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP064598_count.tsv.gz",
        "short_description": "microspores in tissue culture and cold gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP064598_count.tsv.gz",
        "short_description": "microspores in tissue culture and cold gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP064598_count.tsv.gz",
        "short_description": "microspores in tissue culture and cold gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP064598_tpm.tsv.gz",
        "short_description": "microspores in tissue culture and cold gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP064598_tpm.tsv.gz",
        "short_description": "microspores in tissue culture and cold gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP064598_tpm.tsv.gz",
        "short_description": "microspores in tissue culture and cold gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP064598_tpm.tsv.gz",
        "short_description": "microspores in tissue culture and cold gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP064598_count.tsv.gz",
        "short_description": "microspores in tissue culture and cold transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP064598_count.tsv.gz",
        "short_description": "microspores in tissue culture and cold transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP064598_count.tsv.gz",
        "short_description": "microspores in tissue culture and cold transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP064598_count.tsv.gz",
        "short_description": "microspores in tissue culture and cold transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP064598_tpm.tsv.gz",
        "short_description": "microspores in tissue culture and cold transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP064598_tpm.tsv.gz",
        "short_description": "microspores in tissue culture and cold transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP064598_tpm.tsv.gz",
        "short_description": "microspores in tissue culture and cold transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP064598_tpm.tsv.gz",
        "short_description": "microspores in tissue culture and cold transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/PAMP_Triggered_Imune_Response_count.tsv.gz",
        "short_description": "PAMP innoculation of seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/PAMP_Triggered_Imune_Response_count.tsv.gz",
        "short_description": "PAMP innoculation of seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/PAMP_Triggered_Imune_Response_count.tsv.gz",
        "short_description": "PAMP innoculation of seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/PAMP_Triggered_Imune_Response_count.tsv.gz",
        "short_description": "PAMP innoculation of seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/PAMP_Triggered_Imune_Response_tpm.tsv.gz",
        "short_description": "PAMP innoculation of seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/PAMP_Triggered_Imune_Response_tpm.tsv.gz",
        "short_description": "PAMP innoculation of seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/PAMP_Triggered_Imune_Response_tpm.tsv.gz",
        "short_description": "PAMP innoculation of seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/PAMP_Triggered_Imune_Response_tpm.tsv.gz",
        "short_description": "PAMP innoculation of seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/PAMP_Triggered_Imune_Response_count.tsv.gz",
        "short_description": "PAMP innoculation of seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/PAMP_Triggered_Imune_Response_count.tsv.gz",
        "short_description": "PAMP innoculation of seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/PAMP_Triggered_Imune_Response_count.tsv.gz",
        "short_description": "PAMP innoculation of seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/PAMP_Triggered_Imune_Response_count.tsv.gz",
        "short_description": "PAMP innoculation of seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/PAMP_Triggered_Imune_Response_tpm.tsv.gz",
        "short_description": "PAMP innoculation of seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/PAMP_Triggered_Imune_Response_tpm.tsv.gz",
        "short_description": "PAMP innoculation of seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/PAMP_Triggered_Imune_Response_tpm.tsv.gz",
        "short_description": "PAMP innoculation of seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/PAMP_Triggered_Imune_Response_tpm.tsv.gz",
        "short_description": "PAMP innoculation of seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/DRP000768_summary.tsv",
        "short_description": "phosphate starvation in roots and shoots   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/DRP000768_summary.tsv",
        "short_description": "phosphate starvation in roots and shoots   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/DRP000768_summary.tsv",
        "short_description": "phosphate starvation in roots and shoots   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/DRP000768_summary.tsv",
        "short_description": "phosphate starvation in roots and shoots   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/DRP000768_count.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/DRP000768_count.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/DRP000768_count.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/DRP000768_count.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/DRP000768_tpm.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/DRP000768_tpm.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/DRP000768_tpm.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/DRP000768_tpm.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/DRP000768_count.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/DRP000768_count.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/DRP000768_count.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/DRP000768_count.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/DRP000768_tpm.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/DRP000768_tpm.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/DRP000768_tpm.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/DRP000768_tpm.tsv.gz",
        "short_description": "phosphate starvation in roots and shoots transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP068165_summary.tsv",
        "short_description": "seedlings with PEG to simulate drought   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP068165_summary.tsv",
        "short_description": "seedlings with PEG to simulate drought   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP068165_summary.tsv",
        "short_description": "seedlings with PEG to simulate drought   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP068165_summary.tsv",
        "short_description": "seedlings with PEG to simulate drought   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP068165_count.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP068165_count.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP068165_count.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP068165_count.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP068165_tpm.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP068165_tpm.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP068165_tpm.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP068165_tpm.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP068165_count.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP068165_count.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP068165_count.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP068165_count.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP068165_tpm.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP068165_tpm.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP068165_tpm.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP068165_tpm.tsv.gz",
        "short_description": "seedlings with PEG to simulate drought transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP022869_summary.tsv",
        "short_description": "Septoria tritici infected seedlings   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP022869_summary.tsv",
        "short_description": "Septoria tritici infected seedlings   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP022869_summary.tsv",
        "short_description": "Septoria tritici infected seedlings   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP022869_summary.tsv",
        "short_description": "Septoria tritici infected seedlings   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP022869_count.tsv.gz",
        "short_description": "Septoria tritici infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP022869_count.tsv.gz",
        "short_description": "Septoria tritici infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP022869_count.tsv.gz",
        "short_description": "Septoria tritici infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP022869_count.tsv.gz",
        "short_description": "Septoria tritici infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP022869_tpm.tsv.gz",
        "short_description": "Septoria tritici infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP022869_tpm.tsv.gz",
        "short_description": "Septoria tritici infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP022869_tpm.tsv.gz",
        "short_description": "Septoria tritici infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP022869_tpm.tsv.gz",
        "short_description": "Septoria tritici infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP022869_count.tsv.gz",
        "short_description": "Septoria tritici infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP022869_count.tsv.gz",
        "short_description": "Septoria tritici infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP022869_count.tsv.gz",
        "short_description": "Septoria tritici infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP022869_count.tsv.gz",
        "short_description": "Septoria tritici infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP022869_tpm.tsv.gz",
        "short_description": "Septoria tritici infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP022869_tpm.tsv.gz",
        "short_description": "Septoria tritici infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP022869_tpm.tsv.gz",
        "short_description": "Septoria tritici infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP022869_tpm.tsv.gz",
        "short_description": "Septoria tritici infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP043554_summary.tsv",
        "short_description": "Shoots after 2 weeks cold   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP043554_summary.tsv",
        "short_description": "Shoots after 2 weeks cold   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP043554_summary.tsv",
        "short_description": "Shoots after 2 weeks cold   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP043554_summary.tsv",
        "short_description": "Shoots after 2 weeks cold   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP043554_count.tsv.gz",
        "short_description": "Shoots after 2 weeks cold gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP043554_count.tsv.gz",
        "short_description": "Shoots after 2 weeks cold gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP043554_count.tsv.gz",
        "short_description": "Shoots after 2 weeks cold gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP043554_count.tsv.gz",
        "short_description": "Shoots after 2 weeks cold gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP043554_tpm.tsv.gz",
        "short_description": "Shoots after 2 weeks cold gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP043554_tpm.tsv.gz",
        "short_description": "Shoots after 2 weeks cold gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP043554_tpm.tsv.gz",
        "short_description": "Shoots after 2 weeks cold gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP043554_tpm.tsv.gz",
        "short_description": "Shoots after 2 weeks cold gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP043554_count.tsv.gz",
        "short_description": "Shoots after 2 weeks cold transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP043554_count.tsv.gz",
        "short_description": "Shoots after 2 weeks cold transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP043554_count.tsv.gz",
        "short_description": "Shoots after 2 weeks cold transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP043554_count.tsv.gz",
        "short_description": "Shoots after 2 weeks cold transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP043554_tpm.tsv.gz",
        "short_description": "Shoots after 2 weeks cold transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP043554_tpm.tsv.gz",
        "short_description": "Shoots after 2 weeks cold transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP043554_tpm.tsv.gz",
        "short_description": "Shoots after 2 weeks cold transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP043554_tpm.tsv.gz",
        "short_description": "Shoots after 2 weeks cold transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP028357_summary.tsv",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP028357_summary.tsv",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP028357_summary.tsv",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP028357_summary.tsv",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP028357_count.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP028357_count.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP028357_count.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP028357_count.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP028357_tpm.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP028357_tpm.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP028357_tpm.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP028357_tpm.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP028357_count.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP028357_count.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP028357_count.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP028357_count.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP028357_tpm.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP028357_tpm.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP028357_tpm.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP028357_tpm.tsv.gz",
        "short_description": "shoots and leaves of nulli tetra group 1 and group 5 transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP048912_summary.tsv",
        "short_description": "Shoots from NILs segregating for crown rot resistance   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP048912_summary.tsv",
        "short_description": "Shoots from NILs segregating for crown rot resistance   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP048912_summary.tsv",
        "short_description": "Shoots from NILs segregating for crown rot resistance   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP048912_summary.tsv",
        "short_description": "Shoots from NILs segregating for crown rot resistance   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP048912_count.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP048912_count.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP048912_count.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP048912_count.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP048912_tpm.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP048912_tpm.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP048912_tpm.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP048912_tpm.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP048912_count.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP048912_count.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP048912_count.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP048912_count.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP048912_tpm.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP048912_tpm.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP048912_tpm.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP048912_tpm.tsv.gz",
        "short_description": "Shoots from NILs segregating for crown rot resistance transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ERP016738_summary.tsv",
        "short_description": "six unreplicated tissues from Chinese Spring.   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ERP016738_summary.tsv",
        "short_description": "six unreplicated tissues from Chinese Spring.   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ERP016738_summary.tsv",
        "short_description": "six unreplicated tissues from Chinese Spring.   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ERP016738_summary.tsv",
        "short_description": "six unreplicated tissues from Chinese Spring.   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP016738_count.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP016738_count.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP016738_count.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP016738_count.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP016738_tpm.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP016738_tpm.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP016738_tpm.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP016738_tpm.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP016738_count.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP016738_count.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP016738_count.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP016738_count.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP016738_tpm.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP016738_tpm.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP016738_tpm.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP016738_tpm.tsv.gz",
        "short_description": "six unreplicated tissues from Chinese Spring. transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP068156_summary.tsv",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP068156_summary.tsv",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP068156_summary.tsv",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP068156_summary.tsv",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP068156_count.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP068156_count.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP068156_count.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP068156_count.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP068156_tpm.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP068156_tpm.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP068156_tpm.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP068156_tpm.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP068156_count.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP068156_count.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP068156_count.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP068156_count.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP068156_tpm.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP068156_tpm.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP068156_tpm.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP068156_tpm.tsv.gz",
        "short_description": "spikes innoculated with fusarium head blight and ABA/GA transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/developing_spike_count.tsv.gz",
        "short_description": "spikes with water stress gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/developing_spike_count.tsv.gz",
        "short_description": "spikes with water stress gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/developing_spike_count.tsv.gz",
        "short_description": "spikes with water stress gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/developing_spike_count.tsv.gz",
        "short_description": "spikes with water stress gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/developing_spike_tpm.tsv.gz",
        "short_description": "spikes with water stress gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/developing_spike_tpm.tsv.gz",
        "short_description": "spikes with water stress gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/developing_spike_tpm.tsv.gz",
        "short_description": "spikes with water stress gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/developing_spike_tpm.tsv.gz",
        "short_description": "spikes with water stress gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/developing_spike_count.tsv.gz",
        "short_description": "spikes with water stress transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/developing_spike_count.tsv.gz",
        "short_description": "spikes with water stress transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/developing_spike_count.tsv.gz",
        "short_description": "spikes with water stress transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/developing_spike_count.tsv.gz",
        "short_description": "spikes with water stress transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/developing_spike_tpm.tsv.gz",
        "short_description": "spikes with water stress transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/developing_spike_tpm.tsv.gz",
        "short_description": "spikes with water stress transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/developing_spike_tpm.tsv.gz",
        "short_description": "spikes with water stress transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/developing_spike_tpm.tsv.gz",
        "short_description": "spikes with water stress transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP041017_summary.tsv",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP041017_summary.tsv",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP041017_summary.tsv",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP041017_summary.tsv",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP041017_count.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP041017_count.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP041017_count.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP041017_count.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP041017_tpm.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP041017_tpm.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP041017_tpm.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP041017_tpm.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP041017_count.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP041017_count.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP041017_count.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP041017_count.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP041017_tpm.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP041017_tpm.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP041017_tpm.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP041017_tpm.tsv.gz",
        "short_description": "stripe rust and powdery mildew timecourse of infection in seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ERP013983_summary.tsv",
        "short_description": "Stripe rust infected seedlings   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/SRP017303_summary.tsv",
        "short_description": "Stripe rust infected seedlings   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ERP013983_summary.tsv",
        "short_description": "Stripe rust infected seedlings   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/SRP017303_summary.tsv",
        "short_description": "Stripe rust infected seedlings   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ERP013983_summary.tsv",
        "short_description": "Stripe rust infected seedlings   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/SRP017303_summary.tsv",
        "short_description": "Stripe rust infected seedlings   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ERP013983_summary.tsv",
        "short_description": "Stripe rust infected seedlings   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/SRP017303_summary.tsv",
        "short_description": "Stripe rust infected seedlings   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP013983_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP017303_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP013983_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP017303_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP013983_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP017303_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP013983_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP017303_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP013983_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/SRP017303_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP013983_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/SRP017303_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP013983_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/SRP017303_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP013983_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/SRP017303_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP013983_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP017303_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP013983_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP017303_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP013983_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP017303_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP013983_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP017303_count.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP013983_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/SRP017303_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP013983_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/SRP017303_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP013983_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/SRP017303_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP013983_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/SRP017303_tpm.tsv.gz",
        "short_description": "Stripe rust infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ERP013829_summary.tsv",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ERP013829_summary.tsv",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ERP013829_summary.tsv",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ERP013829_summary.tsv",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP013829_count.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP013829_count.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP013829_count.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP013829_count.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP013829_tpm.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP013829_tpm.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP013829_tpm.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP013829_tpm.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP013829_count.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP013829_count.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP013829_count.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP013829_count.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP013829_tpm.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP013829_tpm.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP013829_tpm.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP013829_tpm.tsv.gz",
        "short_description": "timecourse of spikelets inoculated with fusarium head blight transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ERP009837_summary.tsv",
        "short_description": "Zymoseptoria tritici infected seedlings   Summary of number of reads and mapped reads to the IWGSC2.26  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ERP009837_summary.tsv",
        "short_description": "Zymoseptoria tritici infected seedlings   Summary of number of reads and mapped reads to the RefSeq_1.0  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ERP009837_summary.tsv",
        "short_description": "Zymoseptoria tritici infected seedlings   Summary of number of reads and mapped reads to the RefSeq_1.1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ERP009837_summary.tsv",
        "short_description": "Zymoseptoria tritici infected seedlings   Summary of number of reads and mapped reads to the TGACv1  reference by Kallisto."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP009837_count.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP009837_count.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP009837_count.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP009837_count.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings gene counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByGene/ERP009837_tpm.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByGene/ERP009837_tpm.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByGene/ERP009837_tpm.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByGene/ERP009837_tpm.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings gene TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP009837_count.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP009837_count.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP009837_count.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP009837_count.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings transcript counts."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "IWGSC2.26",
        "file": "expvip/IWGSC2.26/ByTranscript/ERP009837_tpm.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.0",
        "file": "expvip/RefSeq_1.0/ByTranscript/ERP009837_tpm.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "RefSeq_1.1",
        "file": "expvip/RefSeq_1.1/ByTranscript/ERP009837_tpm.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings transcript TPMs."
    },
    {
        "project_name": "The transcriptional landscape of polyploid wheat",
        "ploidy": "hexaploid",
        "estimated_size": "16Gb",
        "annot_source": "TGACv1",
        "file": "expvip/TGACv1/ByTranscript/ERP009837_tpm.tsv.gz",
        "short_description": "Zymoseptoria tritici infected seedlings transcript TPMs."
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
