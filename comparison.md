# Output Comparison
The data within ```cleaned_sequences.csv``` that was standardized using the written Python script does agree with all of the data within ```AI_USAGE.md``` that was standardized by the generative AI tool. Both the Python script using regex-based cleaning and the AI tool were also able to produce outputs that are equivalent to that within ```messy_sequences.fasta```. This means that both outputs were about to catch all edge cases and completely clean up the data. That being said, the time and effort put into using each method to produce the correct outputs was dramatically different.

When writting ```clean_up_sequences_regex.py```, multiple trials and edits needed to be made to the regex patterns to produce the final output. One major issue I had was  getting the correct "organism" column output. The 8 sequences all had very different formats for representing the same organism, in addition to different ways to separate between each column. For example, Sample002 formated this portion of the header as "organism:Homo sapiens" with single spaces differentiating each column. Seq6, however, foramted this as "Hsapiens" with "|" separating each column. These differences created many problems with not only reporting the correct organism, but also separating each column. Many trial scripts had to be written and tested to get to the current ```cleaned_sequences.csv```.

Although both outputs were able to eventually report the correct data, there were major differences in the time and effort spent on each. As noted above and within the "Failure Mode Analysis", it took much time and many script changes to correct ```clean_up_sequences_regex.py``` into standardizing the data correctly and completely. On the other hand, it only took inputing 2 prompts into an AI tool to get the same output returned. And the second prompt was only to change the format of the data into a table I could then paste into ```AI_USAGE.md``` so it would be formated better. This second prompt was not to improve the results as the first LLM output was already correct. Due to this, technically the AI-assisted cleaning was the more time efficient method to use in comparison to writing my own Python script.


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