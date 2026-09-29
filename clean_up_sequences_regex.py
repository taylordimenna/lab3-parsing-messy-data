from  pathlib import Path
import csv
import re

#Paths
PROJECT_ROOT = Path(__file__).resolve().parent
FASTA_IN = (PROJECT_ROOT/"messy_sequences.fasta")
CSV_OUT = (PROJECT_ROOT/"cleaned_sequences.csv")

#Separating fastas into header and sequence
def read_fasta(path):
    """Read FASTA records as (header, sequence) pairs."""
    records = []
    header = None
    sequence_parts = []

    with open (path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                if header is not None:
                    records.append(
                        (header, "".join(sequence_parts))
                    )
                header = line[1:].strip()
                sequence_parts = []
            
            else:
                if header is None:
                    raise ValueError(
                        "Sequence found before the first FASTA header"
                    )
                sequence_parts.append(line)

    if header is not None:
        records.append((header, "".join(sequence_parts)))
    return records

#regex patterns
patterns = {
    "sample_id": r"^([^|;\s]+)",
    "organism": (
        r"(?:organism|species)[:=]\s*([\w. ]+)"
        r"(.*?)"
        r"(?=\s+(?:gene|target|len|length)[:=]|[|;]|$)"
    ),
    "gene": r"(?:gene|target)[:=]\s*([\w-]+)",
    "length": r"(?:len|length)[:=]\s*(\d+)\s*(?:bp)?",
    "length_bp": r"b\b(\d+)\s*bp\b",
}

#parsing the fasta
def parse_header(header):
    """Extract metadata from a FASTA header."""

    result = {
        "sample_id": None,
        "organism": None,
        "gene": None,
        "length": None,
    }

    #Get sample_id
    match = re.search(patterns["sample_id"], header)
    if match:
        result["sample_id"] = match.group(1).strip()

    #Get organism
    match = re.search(patterns["organism"], header)
    if match:
        result["organism"] = match.group(1).strip()

    #Get gene
    match = re.search(patterns["gene"], header)
    if match:
        result["gene"] = match.group(1).strip()

    #Get length
    match = re.search(patterns["length"], header)
    if match:
        result["length"] = match.group(1)

    #Lengths written only with number and "bp"
    if result["length"] is None:
        match = re.search(patterns["length_bp"], header)
        if match:
            result["length"] = match.group(1)

    #Header separations with "|"
    parts = [part.strip() for part in header.split("|")]

    if len(parts) >= 3:
        if result["organism"] is None:
            result["organism"] = parts[1]

        if result["gene"] is None:
            gene_candidate = parts[2].strip()

            if re.fullmatch(r"[\w-]+", gene_candidate):
                result["gene"] = gene_candidate

    #Header separations with ";"
    if result["organism"] is None or result["gene"] is None:
        parts = [part.strip() for part in header.split(";")]

        if len(parts) >= 2:
            if result["organism"] is None:
                first_part = re.sub(
                    r"^[^|\s]+(?:\s+)", "", parts[0]
                ).strip()

                if first_part:
                    result["organism"] = first_part

            if result["gene"] is None:
                for part in parts[1:]:
                    if re.fullmatch(r"[\w-]+", part):
                        result["gene"] = part
                        break

    return result

#Writing the csv file
def main():
    records = read_fasta(FASTA_IN)

    fieldnames = [
        "sample_id",
        "organism",
        "gene",
        "length",
        "sequence",
    ]

    with open (CSV_OUT, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for header, sequence in records:
            metadata = parse_header(header)
            if metadata["length"] is None:
                metadata["length"] = len(sequence)
            metadata["sequence"] = sequence
            writer.writerow(metadata)

if __name__ == "__main__":
    main()
