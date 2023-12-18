import json
import os

from Bio import SeqIO

from snapgene_utils import snapgene_file_to_dict, snapgene_file_to_raw_dict

TEST_DIR = os.path.join("tests", "test_samples")
RAW_SNAPSHOT_DIR = os.path.join("tests", "snapshots", "raw")
PRETTY_SNAPSHOT_DIR = os.path.join("tests", "snapshots", "pretty")


def test_snapgene_file_to_raw_dict_simple(tmpdir):
    test_file = os.path.join(TEST_DIR, "AcGFP1.dna")
    snapshot_file = os.path.join(RAW_SNAPSHOT_DIR, "AcGFP1.json")
    file_dict = snapgene_file_to_raw_dict(test_file)
    with open(snapshot_file) as f:
        snapshot = json.loads(f.read())
    assert(snapshot == file_dict)


def test_snapgene_file_to_raw_dict_complex(tmpdir):
    test_file = os.path.join(TEST_DIR, "pGEX-6P-1.dna")
    snapshot_file = os.path.join(RAW_SNAPSHOT_DIR, "pGEX-6P-1.json")
    file_dict = snapgene_file_to_raw_dict(test_file)
    with open(snapshot_file) as f:
        snapshot = json.loads(f.read())
    assert(snapshot == file_dict)


def test_snapgene_file_to_dict_simple(tmpdir):
    test_file = os.path.join(TEST_DIR, "pGEX-6P-1.dna")
    snapshot_file = os.path.join(PRETTY_SNAPSHOT_DIR, "pGEX-6P-1.json")
    file_dict = snapgene_file_to_dict(test_file)
    with open(snapshot_file) as f:
        snapshot = json.loads(f.read())
    assert(snapshot == file_dict)


def test_snapgene_file_to_dict_complex(tmpdir):
    test_file = os.path.join(TEST_DIR, "AcGFP1.dna")
    snapshot_file = os.path.join(PRETTY_SNAPSHOT_DIR, "AcGFP1.json")
    file_dict = snapgene_file_to_dict(test_file)
    with open(snapshot_file) as f:
        snapshot = json.loads(f.read())
    assert(snapshot == file_dict)
