"""
snapgene utils main file
"""
import re
import struct

# import json
import xmltodict
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

try:
    # Biopython <1.78
    from Bio.Alphabet import DNAAlphabet

    has_dna_alphabet = True
except ImportError:
    # Biopython >=1.78
    has_dna_alphabet = False
import html2text
from Bio.SeqFeature import FeatureLocation, SeqFeature

HTML_PARSER = html2text.HTML2Text()
HTML_PARSER.ignore_emphasis = True
HTML_PARSER.ignore_links = True
HTML_PARSER.body_width = 0
HTML_PARSER.single_line_break = True


def parse(val):
    """Parse html."""
    if isinstance(val, str):
        return HTML_PARSER.handle(val).strip().replace("\n", " ").replace('"', "'")
    else:
        return val


def parse_dict(obj):
    """Parse dict in the obj."""
    if isinstance(obj, dict):
        for key in obj:
            if isinstance(obj[key], str):
                obj[key] = parse(obj[key])
            elif isinstance(obj[key], dict):
                parse_dict(obj[key])
    return obj


def to_pretty_snake(s):
    """
    Converts a string to lower snake case. Also removes leading '@', and '_'.
    """
    substituted = s
    if len(substituted) > 0 and substituted[0] == "@":
        substituted = substituted[1:]
    substituted = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', substituted)
    substituted = re.sub('([a-z0-9])([A-Z])', r'\1_\2', substituted).lower()
    if len(substituted) > 0 and substituted[0] == "_":
        substituted = substituted[1:]
    return substituted


def parse_qualifier_dict(raw_qualifier_dict):
    """
    Parses qualifier dicts, as opposed to lists.
    """
    value_obj = raw_qualifier_dict["V"]
    value = None
    if "@int" in value_obj:
        value = int(value_obj["@int"])
    elif "@text" in value_obj:
        value = str(value_obj["@text"])
    if value is None:
        raise ValueError(f"Only @int and @text are supported qualifier types. Found an unsupported qualifier type: {raw_qualifier_dict}.")
    return {raw_qualifier_dict["@name"]: value}
    


def to_pretty_qualifiers(raw_qualifier_obj):
    """
    "Q" keys represent qualifiers. They can be dicts or lists. This function prettifies the format. To standardize things, this will always return a list.

    Here's an example:
    {
      "Q": {
        "@name": "gene",
        "V": {
          "@text": "foo bar baz"
        }
      }
    }

    Here's the output:
    [{
      "gene": "foo bar baz"
    }]
    """
    if isinstance(raw_qualifier_obj, dict):
        return [parse_qualifier_dict(raw_qualifier_obj)]
    elif isinstance(raw_qualifier_obj, list):
        return [
            parse_qualifier_dict(raw_qualifier_dict) for raw_qualifier_dict in raw_qualifier_obj
        ]
    else:
        raise ValueError(f".dna qualifier objects are only dicts or lists. Unsupported type found: {raw_qualifier_obj}")


def to_pretty_dict(d):
    if isinstance(d, list):
        return [to_pretty_dict(i) if isinstance(i, (dict, list)) else i for i in d]
    
    res = {}
    for a, b in d.items():
        if a == "Q":
            res["qualifiers"] = to_pretty_qualifiers(b)
        elif isinstance(b, (dict, list)):
            res[to_pretty_snake(a)] = to_pretty_dict(b)
        else:
            res[to_pretty_snake(a)] = b
    return res


def snapgene_file_to_dict(filepath=None, fileobject=None):
    raw_dict = snapgene_file_to_raw_dict(filepath, fileobject)
    return to_pretty_dict(raw_dict)


def snapgene_file_to_raw_dict(filepath=None, fileobject=None):
    """Return a dictionary containing the data from a ``*.dna`` file.

    Parameters
    ----------
    filepath
        Path to a .dna file created with SnapGene.

    fileobject
        On object-like pointing to the data of a .dna file created with
        SnapGene.
    """
    if filepath is not None:
        fileobject = open(filepath, "rb")

    if fileobject.read(1) != b"\t":
        raise ValueError("Wrong format for a SnapGene file!")

    def unpack(size, mode):
        """Unpack the fileobject."""
        return struct.unpack(">" + mode, fileobject.read(size))[0]

    # READ THE DOCUMENT PROPERTIES
    length = unpack(4, "I")
    title = fileobject.read(8).decode("ascii")
    if length != 14 or title != "SnapGene":
        raise ValueError("Wrong format for a SnapGene file !")

    data = dict(
        isDNA=unpack(2, "H"),
        exportVersion=unpack(2, "H"),
        importVersion=unpack(2, "H"),
        features=[],
        unparsedSections={} # section number -> hex bytes
    )

    while True:
        # READ THE WHOLE FILE, BLOCK BY BLOCK, UNTIL THE END
        next_byte = fileobject.read(1)

        # next_byte table
        # 0: dna sequence
        # 1: compressed DNA
        # 2: unknown
        # 3: unknown
        # 5: primers
        # 6: notes
        # 7: history tree
        # 8: additional sequence properties segment
        # 9: file Description
        # 10: features
        # 11: history node
        # 13: unknown
        # 16: alignable sequence
        # 17: alignable sequence
        # 18: sequence trace
        # 19: Uracil Positions
        # 20: custom DNA colors

        if next_byte == b"":
            # END OF FILE
            break

        block_size = unpack(4, "I")

        if ord(next_byte) == 0:
            # READ THE SEQUENCE AND ITS PROPERTIES
            props = unpack(1, "b")
            data["dna"] = dict(
                topology="circular" if props & 0x01 else "linear",
                strandedness="double" if props & 0x02 > 0 else "single",
                damMethylated=props & 0x04 > 0,
                dcmMethylated=props & 0x08 > 0,
                ecoKIMethylated=props & 0x10 > 0,
                length=block_size - 1,
            )
            data["seq"] = fileobject.read(block_size - 1).decode("ascii")
        elif ord(next_byte) == 5:
            block_content = fileobject.read(block_size).decode("utf-8")
            primers_dict = parse_dict(xmltodict.parse(block_content))
            data["primers"] = primers_dict["Primers"]
        elif ord(next_byte) == 6:
            # READ THE NOTES
            block_content = fileobject.read(block_size).decode("utf-8")
            note_data = parse_dict(xmltodict.parse(block_content))
            data["Notes"] = note_data["Notes"]
        elif ord(next_byte) == 10:
            # READ THE FEATURES
            block_content = fileobject.read(block_size).decode("utf-8")
            feature_data = parse_dict(xmltodict.parse(block_content))
            data["Features"] = feature_data["Features"]
        else:
            b = fileobject.read(block_size)
            data["unparsedSections"][str(ord(next_byte))] = b.hex()
            pass

    fileobject.close()
    return data


def snapgene_file_to_seqrecord(filepath=None, fileobject=None):
    """Return a BioPython SeqRecord from the data of a ``*.dna`` file.

    Parameters
    ----------
    filepath
        Path to a .dna file created with SnapGene.

    fileobject
        On object-like pointing to the data of a .dna file created with
        SnapGene.
    """
    data = snapgene_file_to_raw_dict(filepath=filepath, fileobject=fileobject)
    strand_dict = {"+": 1, "-": -1, ".": 0}

    if has_dna_alphabet:
        seq = Seq(data["seq"], alphabet=DNAAlphabet())
    else:
        seq = Seq(data["seq"])

    seqrecord = SeqRecord(
        seq=seq,
        features=[
            SeqFeature(
                location=FeatureLocation(
                    start=feature["start"],
                    end=feature["end"],
                    strand=strand_dict[feature["strand"]],
                ),
                strand=strand_dict[feature["strand"]],
                type=feature["type"],
                qualifiers=feature["qualifiers"],
            )
            for feature in data["features"]
        ],
        annotations=dict(topology=data["dna"]["topology"], **data["notes"]),
    )

    seqrecord.annotations["molecule_type"] = "DNA"

    return seqrecord


def snapgene_file_to_gbk(read_file_object, write_file_object):
    """Convert a file object."""

    def analyse_gs(dic, *args, **kwargs):
        """Extract gs block in the document."""
        if "default" not in kwargs:
            kwargs["default"] = None

        for arg in args:
            if arg in dic:
                dic = dic[arg]
            else:
                return kwargs["default"]
        return dic

    data = snapgene_file_to_raw_dict(fileobject=read_file_object)
    wfo = write_file_object
    wfo.write(
        (
            "LOCUS       Exported              {0:>6} bp ds-DNA     {1:>8} SYN \
15-APR-2012\n"
        ).format(len(data["seq"]), data["dna"]["topology"])
    )
    definition = analyse_gs(data, "notes", "Description", default=".").replace(
        "\n", "\n            "
    )
    wfo.write("DEFINITION  {}\n".format(definition))
    wfo.write("ACCESSION   .\n")
    wfo.write("VERSION     .\n")
    wfo.write(
        "KEYWORDS    {}\n".format(
            analyse_gs(data, "notes", "CustomMapLabel", default=".")
        )
    )
    wfo.write("SOURCE      .\n")
    wfo.write("  ORGANISM  .\n")

    references = analyse_gs(data, "notes", "References")

    reference_count = 0
    if references:
        for key in references:
            reference_count += 1
            ref = references[key]
            wfo.write(
                "REFERENCE   {}  (bases 1 to {} )\n".format(
                    reference_count, analyse_gs(data, "dna", "length")
                )
            )
            for key2 in ref:
                gb_key = key2.replace("@", "").upper()
                wfo.write("  {}   {}\n".format(gb_key, ref[key2]))

    # generate special reference
    reference_count += 1
    wfo.write(
        "REFERENCE   {}  (bases 1 to {} )\n".format(
            reference_count, analyse_gs(data, "dna", "length")
        )
    )
    wfo.write("  AUTHORS   SnapGeneUtils\n")
    wfo.write("  TITLE     Direct Submission\n")
    wfo.write(
        (
            "  JOURNAL   Exported Monday, Sep 05, 2020 from SnapGene File\
 Utils\n"
        )
    )
    wfo.write(
        "            https://github.com/Edinburgh-Genome-Foundry/SnapGeneReader\n"
    )

    wfo.write(
        "COMMENT     {}\n".format(
            analyse_gs(data, "notes", "Comments", default=".")
            .replace("\n", "\n            ")
            .replace("\\", "")
        )
    )
    wfo.write("FEATURES             Location/Qualifiers\n")

    features = analyse_gs(data, "features")
    for feature in features:
        strand = analyse_gs(feature, "strand", default="")

        segments = analyse_gs(feature, "segments", default=[])
        segments = [x for x in segments if x["@type"] == "standard"]
        if len(segments) > 1:
            line = "join("
            for segment in segments:
                segment_range = analyse_gs(segment, "@range").replace("-", "..")
                if analyse_gs(segment, "@type") == "standard":
                    line += segment_range
                    line += ","
            line = line[:-1] + ")"
        else:
            line = "{}..{}".format(
                analyse_gs(feature, "start", default=" "),
                analyse_gs(feature, "end", default=" "),
            )

        if strand == "-":
            wfo.write(
                "     {} complement({})\n".format(
                    analyse_gs(feature, "type", default=" ").ljust(15), line,
                )
            )
        else:
            wfo.write(
                "     {} {}\n".format(
                    analyse_gs(feature, "type", default=" ").ljust(15), line,
                )
            )
        strand = analyse_gs(feature, "strand", default="")
        # if strand == '-':
        #     wfo.write('                     /direction=LEFT\n')
        # name
        wfo.write(
            '                     /note="{}"\n'.format(
                analyse_gs(feature, "name", default="feature")
            )
        )
        # qualifiers
        for q_key in analyse_gs(feature, "qualifiers", default={}):
            # do not write label, because it has been written at first.
            if q_key == "label":
                pass
            elif q_key == "note":
                for note in analyse_gs(feature, "qualifiers", q_key, default=[]):
                    # do note write color, because it will be written later
                    if note[:6] != "color:":
                        wfo.write('                     /note="{}"\n'.format(note))
            else:
                wfo.write(
                    '                     /{}="{}"\n'.format(
                        q_key, analyse_gs(feature, "qualifiers", q_key, default="")
                    )
                )
        if len(segments) > 1:
            wfo.write(
                (
                    '                     /note="This feature \
has {} segments:'
                ).format(len(segments))
            )
            for seg_i, seg in enumerate(segments):
                segment_name = analyse_gs(seg, "@name", default="")
                if segment_name:
                    segment_name = " / {}".format(segment_name)
                wfo.write(
                    "\n                        {}:  {} / {}{}".format(
                        seg_i,
                        seg["@range"].replace("-", " .. "),
                        seg["@color"],
                        segment_name,
                    )
                )
            wfo.write('"\n')
        else:
            # write colors and direction
            wfo.write(
                21 * " "
                + '/note="color: {}'.format(
                    analyse_gs(feature, "color", default="#ffffff")
                )
            )
            if strand == "-":
                wfo.write('; direction: LEFT"\n')
                # wfo.write('"\n')
            elif strand == "+":
                wfo.write('; direction: RIGHT"\n')
            else:
                wfo.write('"\n')

    # sequence
    wfo.write("ORIGIN\n")
    seq = analyse_gs(data, "seq")
    # divide rows
    for i in range(0, len(seq), 60):
        wfo.write(str(i).rjust(9))
        for j in range(i, min(i + 60, len(seq)), 10):
            wfo.write(" {}".format(seq[j : j + 10]))
        wfo.write("\n")
    wfo.write("//\n")
