"""
snapgene_reader module
usage:
    from snapgene_utils import snapgene_file_to_raw_dict
    obj = snapgene_file_to_raw_dict(file_path='test.dna')
"""
from .snapgene_reader import (
    snapgene_file_to_dict,
    snapgene_file_to_gbk,
    snapgene_file_to_raw_dict,
    snapgene_file_to_seqrecord,
)
