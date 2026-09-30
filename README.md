# Lab 3 Parsing Messy Data
Contains my work for Lab 3: Parsing Messy Data

## Project Overview
This project compares two approaches to structuring a messy FASTA file. This FASTA file contains 8 sequences with inconsistantly formatted headers. The two approaches used are: a written Python script with regex patterns, and a generative AI tool. Both approaches clean the same messy FASTA file into structured output tables.

## Setup
### 1. Clone the repository to your local computer.
Run the following command:

    git clone https://github.com/taylordimenna/lab3-parsing-messy-data.git

### 2. Move into repository
Run the following command:

    cd lab3-parsing-messy-data

You are now inside the ```lab3-parsing-messy-data``` directory.

### 3. Verify Python
Python is required to run the script. To check and confirm that Python is available, run the following command:

    python --version

### 4. Run Python script
To run ```clean_up_sequences_regex.py```, run the following command:

    python clean_up_sequences_regex.py

This script reads ```messy_sequences.fasta``` and parses it into a cleaned CSV output within ```cleaned_sequences.csv```.

## Repository Contents
```.gitignore``` contains the files that should not be committed to the repository. In this case, there are none located within it.

```AI_USAGE.md``` contains information about any AI tools used to help complete this lab, and the AI-assisted cleaning portion of this project.

```clean_up_sequences_regex.py``` is the Python script that codes for the creation of ```cleaned_sequences.csv ``` with regex-based cleaning.

```cleaned_sequences.csv``` is the output CSV file for ```clean_up_sequences_regex.py``` which contains the structured FASTA file data.

```comparison.md``` contains the output comparison and failure mode analysis portions of this project.

```messy_sequences.fasta``` is a FASTA file that contains 8 sequences with messy/inconsistent header formats. This is the input dataset that is 'cleaned' with ```clean_up_sequences_regex.py```.