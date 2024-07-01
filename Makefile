# Makefile for ETL dependency chain
PYTHONPATH=nasa_interview_project/
export PYTHONPATH

ingest_file=nasa_interview_project/pipeline/ingest.py
analyze_file=nasa_interview_project/pipeline/analyze.py
visualize_file=nasa_interview_project/pipeline/visualize.py 

# Define the targets
all: visualize

ingest: 
	python3 $(ingest_file)

analyze: ingest $(analyze_file)
	python3 $(analyze_file)

visualize: analyze $(visualize_file)
	@echo "Running visualization script..."
	panel serve $(visualize_file)

clean:
	@echo "Cleaning up..."
	rm nasa_interview_project/data/CountyCrossWalk_Zillow.csv nasa_interview_project/data/joined_zillow_svi.csv nasa_interview_project/data/zillow_new_home.csv

test:
	pytest tests/

generate-requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

.PHONY: all ingest analyze visualize clean