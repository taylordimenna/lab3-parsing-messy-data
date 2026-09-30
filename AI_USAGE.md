# AI Usage within ```clean_up_sequences_regex.py```
## Model used:
ChatGPT (GPT-5.6 Luna)

## Error
Within my CSV file, samples 2 and 8 had portions of the "gene" column being put into the "organism" column.

    Sample002,Homo sapiens gene,TP53,134,

    sample-8,Homo_sapiens gene,TP53,123,

Instead of the organism being parsed as "Homo sapiens" and "Homo_sapiens", the word "gene" was also being included.

## What this error means
This was occuring because of the way that the headers within ```messy_sequences.fasta``` were formatted. For both samples, the separation between the organism and the gene were only a single space.

## Existing script
Before using AI to help me correct this mistake, I had the following as my regex pattern for "organism":

    patterns = {
            "organism": (
            r"(?:organism|species)[:=]\s*([\w. ]+)"
            r"(.*?)"
            r"(?=\s+(?:gene|target|len|length)[:=]|[|;]|$)"
        ),
    }

## Prompt
The prompt I typed into the LLM to allow me to correct this parsing mistake was:

    "I am writing a Python script with regex patterns to clean a messy FASTA file with 8 sequences. My existing regex patterns for one of the columns is the following: [I pasted the script located above in 'Existing script']. Within the created CSV file, a term belonging to the next column ("gene") is being parsed next to the reported 'organism' in the table. This is due to the fact that the existing FASTA file headers separates these columns by a single space. Please tell me what I need to change within my existing script to address this issue and separate these columns."

## Output
The LLM then returned an output explaining that I was combining two patterns. The first ([\w. ]+) was capturing the organism with "gene" before the other pattern written (?=\s+(?:gene|target|len|length)[:=]|[|;]|$) had a chance to separate them. It suggested that I removed ([\w. ]+) to address the issue.

## Verifying the fix
After receiving this suggestion, I checked the "Quick reference" table located within the README of ```week04-text-processing``` in the applied-computing-HDS repository to confirm that I understood what its suggestion would accomplish. I then made the edit within my script and ran it again. The CSV file created by the updated script ended up containing the fixed data, and so I kept the change within the script.

# AI-Assisted Cleaning
## Model used: 
ChatGPT (GPT-5.6 Luna)

## Prompt:
    "Here is a FASTA file with 8 sequences. Please extract and clean the fields into one CSV table. Here is the complete FASTA file: 
    [I pasted the entire contents of messy_sequences.fasta here]"

## Output:
    Absolutely. I’ll normalize the inconsistent FASTA headers into consistent fields and keep the sequence itself as a single cleaned field. I’ll also preserve missing/unknown values rather than guessing them. 👍
    
    sample_id	organism	    gene	length	    note	       sequence
    sample_001	Homo_sapiens	BRCA1	120		                   CTAAAGACAATTACATAACATACACGTCAGCACGAAACTTGTTGGCCCAGTGTGAATCGC...
    Sample002	Homo_sapiens	TP53			                   GGCATTTTTATTACACTCAGAAACAGAACTCGGGTAATTTTGACAGGTCACGCAGAGGCG...
    sample-003	Homo_sapiens	EGFR	150		                   TTCCATCACCCTAAGTAACCGAATAATGCGTTCGCTCTATTGACTACGACGCGCTCATTC...
    SAMPLE_004	H.sapiens	    BRCA1			                   GTCAATGCGATCCGTAGGGGCAGCGCAGTATGCCAAGACTATAGGCACTGTCGCATCACA...
    sample005	Homo sapiens	TP53	130		                   CTGGTTTACGATAGTATGTCCAACGGCGAGCTTTACATTTGCTGTGAGAGGTACAGGGAT...
    seq6	    Hsapiens	    EGFR			                   TTGACATTTAATTTCACCCATAAACCAGCGTAAAGCTGCAAGTGGCTCCATGAACTTAGC...
    Sample_007	Homo_sapiens	BRCA1		        re-sequenced   CTGGTAATCGTCGGTATCTATATAAGCAGGGGAGGGGAAACATTTGTTCTCAGCCGGTGA...
    sample-8	Homo_sapiens	TP53	NA		                   GCACGACAGTGCGACATTATATCACTGTGGTAGGTTAGCTTCATCTAATGTCCAACTAGC...

    I can also give you the complete CSV with all sequences (not truncated like the display above) as a downloadable .csv file.

## Second prompt:
    Would you be able to make that into a table I could paste into an md file?

## Second output:
    Yes - here's the complete Markdown table with the sequences included in full. You can copy/paste this directly into a .md file.
| sample_id | organism | gene | length | note | sequence |
|---|---|---|---:|---|---|
| sample_001 | Homo_sapiens | BRCA1 | 120 | | CTAAAGACAATTACATAACATACACGTCAGCACGAAACTTGTTGGCCCAGTGTGAATCGCTTAAGGGTTAAGTAAGTGTGATGCATACGCCTTTACTTGCTGTGTCCACCCCATCGGACT |
| Sample002 | Homo_sapiens | TP53 | | | GGCATTTTTATTACACTCAGAAACAGAACTCGGGTAATTTTGACAGGTCACGCAGAGGCGCGCCCTCCTGAAGTGCGTGGACACTCGCTATGAATCTCTGATTTACCCACTCTGCCAAACTCCAGCGCGGTCAG |
| sample-003 | Homo_sapiens | EGFR | 150 | | TTCCATCACCCTAAGTAACCGAATAATGCGTTCGCTCTATTGACTACGACGCGCTCATTCCCTTGTCGGAGAGTTATGGAACAAGGACGCTGTCTGAGACTAGAAGACAGATAGTGCACACGACCGGCGTCGGAGAAACTCTATTTGCCGCCTGACA |
| SAMPLE_004 | H.sapiens | BRCA1 | | | GTCAATGCGATCCGTAGGGGCAGCGCAGTATGCCAAGACTATAGGCACTGTCGCATCACAAACGATTAACTGATAAATGAGCCCTTTATGACACGGGCATATGA |
| sample005 | Homo sapiens | TP53 | 130 | | CTGGTTTACGATAGTATGTCCAACGGCGAGCTTTACATTTGCTGTGAGAGGTACAGGGATTAGTGAGAAGCCGTGCGTATCAATTCGTACCTTGGGGGTCGTTACCACTCTGTTCCCACGAGCGGCATTTCTGGATGGCCAGCT |
| seq6 | Hsapiens | EGFR | | | TTGACATTTAATTTCACCCATAAACCAGCGTAAAGCTGCAAGTGGCTCCATGAACTTAGCTGCTAGTGTCAGACTCGCCTCGGATCCTTACTACACTAACTTGAACGCCTAGTGGTCAAAGAGTA |
| Sample_007 | Homo_sapiens | BRCA1 | | re-sequenced | CTGGTAATCGTCGGTATCTATATAAGCAGGGGAGGGGAAACATTTGTTCTCAGCCGGTGACTCCTAATGCTAAGACATTTCCCTTCAGGGGGGGCTCCCCCGCGATGCCATAAATCTGAGCAACCAGCTGAAGCA |
| sample-8 | Homo_sapiens | TP53 | NA | | GCACGACAGTGCGACATTATATCACTGTGGTAGGTTAGCTTCATCTAATGTCCAACTAGCCGGCCAATTCGCATGATACCTCTCCATCTGACCCAAGATTGTGCTTGTTCAATTCTTCTTAAC |