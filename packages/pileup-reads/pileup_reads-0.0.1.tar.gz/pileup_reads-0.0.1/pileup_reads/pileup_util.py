import array
import logging
import math
import os
import shutil

from .bam_util import Header, iter_intervals
from .check_util import check_choice, check_executable, check_number, check_path
from .util import all_same, parallelize, pipe, with_tmp_dir, z_format, z_open

logging.basicConfig(format="%(message)s", level=logging.INFO)
log = lambda message: logging.info(message)


def pilup_intervals(intervals, start, end, bin_size):
    pileup = array.array("f", [0]) * math.ceil((end - start) / bin_size)
    count = 0
    for interval in intervals:
        if interval[0] >= end:
            continue
        if interval[0] < start:
            if interval[1] <= start:
                continue
            interval = (start, interval[1])
            count -= 1
        if interval[1] > end:
            interval = (interval[0], end)
        index_start = (interval[0] - start) // bin_size
        index_end = math.ceil((interval[1] - start) / bin_size)
        if index_end == index_start:
            index_end += 1
        for index in range(index_start, index_end):
            pileup[index] += 1
        count += 1
    return pileup, count


def write_pileup(path, pileup, overwrite=True):
    mode = "wb" if overwrite else "ab"
    with z_open(path, mode) as file:
        array.array("Q", [len(pileup)]).tofile(file)
        pileup.tofile(file)


def read_pileup(path, remove=False):
    with z_open(path, "rb") as file:
        length = array.array("Q")
        length.fromfile(file, 1)
        length = length[0]
        pileup = array.array("f")
        pileup.fromfile(file, length)
    if remove:
        os.remove(path)
    return pileup


def pilup_intervals_process(in_path, out_path, chr_id, start, end, bin_size, read_length, def_value):
    intervals = iter_intervals(in_path, chr_id, start, end, read_length)
    pileup, intervals_count = pilup_intervals(intervals, start, end, bin_size)
    pileup_log_sum = 0
    pileup_sum_count = 0
    for index, value in enumerate(pileup):
        if value > 0:
            pileup_log_sum += math.log2(value)
            pileup_sum_count += 1
        else:
            pileup[index] = def_value
    write_pileup(out_path, pileup)
    return intervals_count, pileup_log_sum, pileup_sum_count


def merge_pileups_to_bedgraph(in_paths, out_path, chr_id, start, chr_size, bin_size, norm_factor):
    entry = [None, None, None]
    with z_open(out_path, "w", 1) as out_file:
        for in_path in in_paths:
            pileup = read_pileup(in_path, remove=True)
            for value in pileup:
                value *= norm_factor
                if value != entry[2]:
                    if entry[2] is not None:
                        out_file.write(f"{chr_id}\t{entry[0]}\t{entry[1]}\t{entry[2]}\n")
                    entry = [start, min(start + bin_size, chr_size), value]
                else:
                    entry[1] += bin_size
                start += bin_size
        if entry[2] is not None:
            out_file.write(f"{chr_id}\t{entry[0]}\t{entry[1]}\t{entry[2]}\n")


def merge_pileups_to_wig(in_paths, out_path, chr_id, start, chr_size, bin_size, norm_factor):
    with z_open(out_path, "w", 1) as out_file:
        for in_path in in_paths:
            pileup = read_pileup(in_path, remove=True)
            chunk_size = bin_size * len(pileup)
            if chunk_size == 0:
                continue
            if start + chunk_size > chr_size:
                pileup = pileup[:(chr_size - start) // bin_size]
                chunk_size = bin_size * len(pileup)
            if all_same(pileup):
                out_file.write(f"fixedStep chrom={chr_id} start={start + 1} step={chunk_size} span={chunk_size}\n")
                out_file.write(f"{pileup[0]}\n")
                start += chunk_size
                continue
            out_file.write(f"fixedStep chrom={chr_id} start={start + 1} step={bin_size} span={bin_size}\n")
            out_file.write("\n".join(str(value * norm_factor) for value in pileup))
            out_file.write("\n")
            start += chunk_size


def merge_pileups_process(dir_path, out_format, chr_index, chr_id, chr_size, chunk_size, bin_size, norm_factor):
    if out_format in ["bedgraph", "bedgraph.gz"]:
        merging_function = merge_pileups_to_bedgraph
    elif out_format in ["wig", "wig.gz"]:
        merging_function = merge_pileups_to_wig
    else:
        raise ValueError(f"invalid output format: {out_format}")
    in_paths = (
        f"{dir_path}/pilup.{chr_index}.{start}"
        for start in range(0, chr_size, chunk_size))
    out_path = f"{dir_path}/chr.{chr_index}.{out_format}"
    merging_function(in_paths, out_path, chr_id, 0, chr_size, bin_size, norm_factor)


@with_tmp_dir
def pileup(
    in_path, out_path, tmp_dir,
    bin_size=10, read_length=150, chunk_size=1000000, def_value=0,
    normalize="count", out_format=None, parallel=1):

    in_path = check_path(in_path, exist="file")
    out_path = check_path(out_path, exist="parent")
    tmp_dir = check_path(tmp_dir, exist="dir")
    bin_size = check_number(bin_size, min=1, type=int)
    read_length = check_number(read_length, min=1, type=int)
    chunk_size = check_number(chunk_size, min=1, divisible=bin_size, type=int)
    normalize = check_choice(normalize,
        choices=["count", "cpm", "bpm", "enrichment"])
    out_format = check_choice(out_format,
        choices=["wig", "wig.gz", "bedgraph", "bedgraph.gz", "bigwig"],
        if_none=z_format(out_path))
    parallel = check_number(parallel, min=1, type=int)

    pre_format = "wig.gz" if out_format == "bigwig" else out_format
    executables = ["samtools"]
    if out_format == "bigwig":
        if "wig" in pre_format:
            executables.append("wigToBigWig")
        if "bedgraph" in pre_format:
            executables.append("bedGraphToBigWig")
    check_executable(*executables)
    header = Header.read_file(in_path)
    chr_sizes = header.chr_sizes

    log(f"pileup reads from {in_path}")
    tasks = []
    reads_count, log_sum, sum_count = 0, 0, 0
    for chr_index, (chr_id, chr_size) in enumerate(chr_sizes.items()):
        for start in range(0, chr_size, chunk_size):
            end = min(start + chunk_size, chr_size)
            path = f"{tmp_dir}/pilup.{chr_index}.{start}"
            tasks.append([
                in_path, path, chr_id, start, end,
                bin_size, read_length, def_value])
    for result in parallelize(tasks, parallel, pilup_intervals_process):
        reads_count += result[0]
        log_sum += result[1]
        sum_count += result[2]
    if normalize == "cpm":
        norm_factor = 1000000 / reads_count
    elif normalize == "bpm":
        norm_factor = 1000000 / 2 ** (log_sum)
    elif normalize == "enrichment":
        norm_factor = 1 / 2 ** (log_sum - math.log2(sum_count))
    else:
        norm_factor = 1
    log(f"reads: {reads_count}, normalization: {normalize} {norm_factor}")

    log("merge pileups")
    tasks = []
    for chr_index, (chr_id, chr_size) in enumerate(chr_sizes.items()):
        tasks.append([
            tmp_dir, pre_format, chr_index, chr_id, chr_size,
            chunk_size, bin_size, norm_factor])
    result = list(parallelize(tasks, parallel, merge_pileups_process))

    log(f"make output as {out_path}")
    merged_path = f"{tmp_dir}/merged.{pre_format}" \
        if out_format == "bigwig" \
        else out_path
    with z_open(merged_path, "wb") as file:
        for chr_index, _ in enumerate(chr_sizes.items()):
            pre_path = f"{tmp_dir}/chr.{chr_index}.{pre_format}"
            with z_open(pre_path, "rb") as pre_file:
                shutil.copyfileobj(pre_file, file)
            os.remove(pre_path)
    if out_format == "bigwig":
        chr_path = header.write_chr_sizes(f"{tmp_dir}/chr_sizes")
        executable = ("wig" if "wig" in pre_format else "bedGraph") + "ToBigWig"
        with pipe([executable, merged_path, chr_path, out_path]) as _:
            pass
