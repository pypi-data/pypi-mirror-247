from .util import pipe


class Header:

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    @classmethod
    def read_file(cls, path):
        data = dict(HD=[], SQ=[], RG=[], PG=[], CO=[])
        command = ["samtools", "view", "-H", path]
        with pipe(command) as stdout:
            for line in stdout:
                line = line.rstrip()
                if not line:
                    continue
                record_type, record = line[1:3], line[4:]
                if record_type != "CO":
                    record = record.split("\t")
                    record = dict(entry.split(":", 1) for entry in record)
                data[record_type].append(record)
            data["HD"] = data["HD"][0] if data["HD"] else {}
        return cls(data)

    @property
    def chr_sizes(self):
        return dict(sorted(
            ((entry["SN"], int(entry["LN"])) for entry in self["SQ"]),
            key=lambda entry: entry[0]))

    def write_chr_sizes(self, path):
        with open(path, "w") as file:
            for chr_id, chr_size in self.chr_sizes.items():
                file.write(f"{chr_id}\t{chr_size}\n")
        return path


class Cigar:

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "".join(
            symbol if count == 1 else f"{count}{symbol}"
            for symbol, count in self.data)

    @classmethod
    def read_string(cls, string):
        data = []
        index = len(string) - 1
        while index >= 0:
            symbol = string[index]
            count = 0
            base = 1
            index -= 1
            while index >= 0 and string[index] in "0123456789":
                count += int(string[index]) * base
                base *= 10
                index -= 1
            data.append([symbol, count or 1])
        return cls(reversed(data))

    @property
    def ref_length(self):
        length = 0
        for symbol, count in self.data:
            if symbol in "MDN=X":
                length += count
        return length

    @property
    def qry_length(self):
        length = 0
        for symbol, count in self.data:
            if symbol in "MIS=X":
                length += count
        return length


def iter_reads(path, chr_id, start, end):
    # bam file must be indexed
    command = ["samtools", "view", path, f"{chr_id}:{start + 1}-{end}"]
    with pipe(command) as stdout:
        for line in stdout:
            yield line.rstrip().split("\t")


def iter_intervals(path, chr_id, start, end, read_length):
    for read in iter_reads(path, chr_id, start, end):
        flag = int(read[1])
        if flag & 0x4 or flag & 0x100 or flag & 0x800:
            continue # unmapped, secondary or supplementary alignment
        if flag & 0x1: # paired
            if not (flag & 0x40) ^ (flag & 0x80):
                continue # not first in pair xor last in pair
            if flag & 0x8 or not flag & 0x2:
                continue # mate unmapped or not properly paired
            if flag & 0x10: # reverse complement
                cigar = Cigar.read_string(read[5])
                length = cigar.ref_length
                end = int(read[3]) - 1 + length
                start = end + int(read[8])
            else:
                start = int(read[3]) - 1
                end = start + int(read[8])
            if start > end:
                continue
        else:
            cigar = Cigar.read_string(read[5])
            length = cigar.ref_length
            if flag & 0x10: # reverse complement
                end = int(read[3]) - 1 + length
                start = end - (read_length or length)
            else:
                start = int(read[3]) - 1
                end = start + (read_length or length)
        yield [start, end]
