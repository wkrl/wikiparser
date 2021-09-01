SHELL=/bin/bash
VERSION=1.0.0

max_length = 100
output_file = 'wikipedia-$(max_length)chars.json'

kb: fetch extract parse_without_annotations merge

kb_annotated: fetch extract parse_with_annotations merge

fetch:
	pip3 install -r requirements.txt
	python3 download_data.py

extract:
	python3 -m wikiextractor.WikiExtractor *.xml.* --output ./extracted --links --json --quiet --filter_disambig_pages
	
parse_with_annotations: 
	mkdir -p parsed
	python3 wikiextractor_to_texoo.py --annotate

parse_without_annotations:
	mkdir -p parsed
	python3 wikiextractor_to_texoo.py --max_length $(max_length)

merge: 
	python3 merge_datasets.py --output ${output_file}

clean:
	rm -rf extracted
	rm -rf parsed
	rm -f ${output_file}

