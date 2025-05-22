# solr-vufind
# Solr Language Field Updater

A Python script for updating language fields in a Solr index based on a mapping file.

## Description

This script connects to a Solr instance and updates language field values according to mappings defined in a `language_mapping.txt` file. It's designed to handle bulk updates efficiently with configurable batch sizes.

## Features

- Processes language mappings from a simple text file
- Updates documents in configurable batch sizes (default: 1000)
- Only updates documents where the language exactly matches the source value
- Provides progress reporting
- Handles commit behavior carefully

## Requirements

- Python 3.x
- pysolr library (`pip install pysolr`)
- Access to a Solr instance

## Configuration

1. Edit the Solr connection URL in the script:
   ```python
   solr = pysolr.Solr('http://localhost:8983/solr/biblio', always_commit=False)
2. Create a language_mapping.txt file with your language mappings in the format:
   ```python
   old_language_code = new_language_code


## Usage
1. Install dependencies:
```python
pip install pysolr

2. Prepare your language_mapping.txt file

3. Run the script:
```python
python update_languages.py
