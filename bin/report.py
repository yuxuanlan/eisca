#!/usr/bin/env python

import dominate.tags as html
import ezcharts as ezc
from ezcharts.components.reports.labs import LabsReport, LabsAddendum
from ezcharts.layout.snippets import DataTable, Grid, Tabs
from ezcharts.components.theme import LAB_head_resources

import argparse
from pathlib import Path
from report_util import *
import util
import json
import pandas as pd
import sys


logger = util.get_named_logger('Report')

report_title = 'EI Single Cell Analysis Report'
workflow_name = 'eisca'


def parse_args(argv=None):
    """Define and immediately parse command line arguments."""

    parser = argparse.ArgumentParser(
        description="Quality control before and after cell filtering",
        # epilog="python count_reads_from_bam.py --bam file.bam --bed file.bed --json output.json",
    )
    parser.add_argument("report", help="Report output file")
    # parser.add_argument(
    #     "--samplesheet",
    #     metavar="FILE_SAMPLESHEET",
    #     type=Path,
    #     help="Input samplesheet file.",
    #     required=True,
    # )
    parser.add_argument(
        "--results",
        metavar="RESULTS_DIR",
        type=Path,
        help="Results directory.",
        required=True,
    )
    # parser.add_argument(
    #     "--stats", nargs='+',
    #     help="Fastcat per-read stats, ordered as per entries in --metadata.")
    # parser.add_argument(
    #     "--images", nargs='+',
    #     help="Sample directories containing various images to put in report")
    # parser.add_argument(
    #     "--survival",
    #     help="Read survival data in TSV format")
    parser.add_argument(
        "--params",
        metavar="FILE_PARAMS",
        type=Path,
        help="Workflow params json file",
        required=True,
    )
    parser.add_argument(
        "--versions",
        metavar="FILE_VERSIONS",
        type=Path,
        help="Workflow versions file",
        required=True,
    )
    # parser.add_argument(
    #     "--umap_dirs", nargs='+',
    #     help="Sample directories containing umap and gene expression files")
    # parser.add_argument(
    #     "--umap_genes", help="File containing list of genes to annnotate UMAPs")
    # parser.add_argument(
    #     "--metadata", default='metadata.json', required=True,
    #     help="sample metadata")
    parser.add_argument(
        "--wf_version", default='unknown',
        help="version of the executed workflow")               
    return parser.parse_args(argv)


def main(argv=None):
    logger.info('Building report')
    args = parse_args(argv)


    if not args.params.is_file():
        logger.error(f"The given input file {args.params} was not found!")
        sys.exit(2)

    if not args.versions.is_file():
        logger.error(f"The given input file {args.versions} was not found!")
        sys.exit(2)

    report = LabsReport(
        report_title, workflow_name,
        args.params, args.versions, args.wf_version,
        head_resources=[*LAB_head_resources])
    
    report.banner.clear()
    report.footer.clear()
    report.intro_content.add(EIBanner(report_title, workflow_name))
    report.footer.add(EILabsAddendum(workflow_name, args.wf_version))

    # samplesheet = pd.read_csv(args.samplesheet)
    # samples = samplesheet['sample'].unique()

    path_quant_qc = Path(args.results, 'quant_qc')
    path_quant_qc_scatter = Path(path_quant_qc, 'scatter')
    path_quant_qc_violin = Path(path_quant_qc, 'violin')
    path_cell_filtering = Path(args.results, 'cell_filtering')

    if path_quant_qc.exists():
        with report.add_section('Quantification QC', 'quant_QC'):
            html.p("""This section shows the QC plots of counts from alignment and quantification steps.""")
            plots_from_image_files(path_quant_qc_scatter, meta='sample', widths=['800'])
            plots_from_image_files(path_quant_qc_violin, meta='sample')
    else:
        logger.info('Skipping Quantification QC')

    if path_quant_qc.exists():
        with report.add_section('Cell filtering', 'cell_filtering'):
            html.p("""This section shows the QC plots after filtering cells.""")
            plots_from_image_files(path_cell_filtering, widths=['800'])            
            plots_from_image_files(path_cell_filtering, meta='sample')            
    else:
        logger.info('Skipping Cell filtering')

    # html.script('document.getElementsByTagName("p")[0].innerHTML("test cool")')
    # report.banner.getElementsByTagName('p')[0]

    report.write(args.report)
    logger.info('Report writing finished')
    

if __name__ == "__main__":
    sys.exit(main())