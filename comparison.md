# Output Comparison



# Failure Mode Analysis
## First Error in Written Python Script
The first record where the written Python script got something wrong was when initially, two samples had the word "gene" being reported within the "organism" column. This example was addressed in more detail within ```AI_USAGE.md```, but it was ultimately caused by an error in the written redex pattern for the "organism" column.

**The error was:**

| sample_id | organism | gene | length | sequence |
|---|---|---|---:|---|
| Sample002 | Homo_sapiens gene| TP53 | 134 | GGCATTTTTATTACACTCAGAAACAGAACTCGGGTAATTTTGACAGGTCACGCAGAGGCGCGCCCTCCTGAAGTGCGTGGACACTCGCTATGAATCTCTGATTTACCCACTCTGCCAAACTCCAGCGCGGTCAG |
| sample-8 | Homo_sapiens gene| TP53 | 123 | GCACGACAGTGCGACATTATATCACTGTGGTAGGTTAGCTTCATCTAATGTCCAACTAGCCGGCCAATTCGCATGATACCTCTCCATCTGACCCAAGATTGTGCTTGTTCAATTCTTCTTAAC |

**Script causing the error:**

    patterns = {
            "organism": (
            r"(?:organism|species)[:=]\s*([\w. ]+)"
            r"(.*?)"
            r"(?=\s+(?:gene|target|len|length)[:=]|[|;]|$)"
        ),
    }

The reason for this error was the extra ([\w. ]+) within the regex pattern. In order to address this, the ([\w. ]+) was removed.

**Fixed script:**

    patterns = {
         "organism": (
          r"(?:organism|species)[:=]\s*"
         r"(.*?)"
         r"(?=\s+(?:gene|target|len|length)[:=]|[|;]|$)"
        ),
    }

**Fixed output:**

| sample_id | organism | gene | length | sequence |
|---|---|---|---:|---|
| Sample002 | Homo_sapiens | TP53 | 134 | GGCATTTTTATTACACTCAGAAACAGAACTCGGGTAATTTTGACAGGTCACGCAGAGGCGCGCCCTCCTGAAGTGCGTGGACACTCGCTATGAATCTCTGATTTACCCACTCTGCCAAACTCCAGCGCGGTCAG |
| sample-8 | Homo_sapiens | TP53 | 123 | GCACGACAGTGCGACATTATATCACTGTGGTAGGTTAGCTTCATCTAATGTCCAACTAGCCGGCCAATTCGCATGATACCTCTCCATCTGACCCAAGATTGTGCTTGTTCAATTCTTCTTAAC |

At the time of this error, there were also more errors within the reported "length" column and no "note" column was created yet. These were addressed later on.

## Second Error in Written Python Script
The second record where the written Python script got something wrong was when I did not write any code for the "note" column. I didn't notice that one of the sample sequences (sample 7) had a note until I was doing a final run through comparing ```cleaned_sequences.csv``` to ```messy_sequences.fasta```. It was only then that I realized I had missed an entire column.

**Fixed script:**

The addition of the following code allowed this column to be created within the CSV file.

On line 54:

    patterns = {
    "note": r"note[:=]\s*([^|;]+)",
    }

On line 66:

    result = {
        "note": None,
    }

On lines 95-97:

    match = re.search(patterns["note"], header)
    if match:
        result["note"] = match.group(1).strip()

One line 142:

    fieldnames =[
        "note",
    ]


**Fixed output:**

By adding this code to ```clean_up_sequences_regex.py```, I was able to also parse the "note" column within ```cleaned_sequences.csv```.