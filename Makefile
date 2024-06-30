# Makefile for ETL dependency chain
PYTHONPATH=nasa_interview_project/
export PYTHONPATH

ingest_file=nasa_interview_project/pipeline/ingest.py
analyze_file=nasa_interview_project/pipeline/analyze.py
visualize_file=nasa_interview_project/pipeline/visualize.py 

# Define the targets
all: visualize

ingest: 
	python $(ingest_file)

analyze: ingest $(analyze_file)
	python $(analyze_file)

visualize: analyze $(visualize_file)
	@echo "Running visualization script..."
	panel serve $(visualize_file)

clean:
	@echo "Cleaning up..."
	# Add any cleanup commands here
	# e.g., rm -f *.o

test:
	pytest tests/

.PHONY: all ingest analyze visualize clean