# Define the Python interpreter to use
ENV = C:/ProgramData/Miniconda3/envs/route11
PDF_FOLDER = "."
BIB :=
INTERPRETER = $(ENV)/python

# Pandoc options
PANDOC_TEMPLATE = eisvogel
PANDOC_OPTIONS_COMMON = -s --listings --citeproc --metadata-file=metadata.yaml -V mainfont="Times New Roman"
PANDOC_OPTIONS = $(PANDOC_OPTIONS_COMMON) --number-sections --template=eisvogel
PANDOC_OPTIONS_HTML = $(PANDOC_OPTIONS_COMMON) --lua-filter=parse-html.lua
PANDOC_OPTIONS_DOC = $(PANDOC_OPTIONS_COMMON) --webtex --reference-doc="template.docx"

# Define a list of Python scripts to execute
SCRIPTS = report

# Find all Markdown and text files in the current directory
MARKDOWN_FILES := $(wildcard *.md)
TEXT_FILES := $(wildcard *.txt)

# Define the base names for the output files
# BASE_NAMES = PVD_review hypo_B_review  
BASE_NAMES = settlement_assessment

# Define the output file extensions
EXTENSIONS = pdf docx

# Define the default target
.DEFAULT_GOAL := ALL

ALL: $(foreach name,$(BASE_NAMES),$(foreach ext,$(EXTENSIONS),$(name).$(ext)))

$(info MARKDOWN_FILES=$(MARKDOWN_FILES))


# Pattern rule to generate Markdown to PDF conversion
%.pdf: %.txt
	pandoc $^ $(PANDOC_OPTIONS) -o $@

# Pattern rule to generate Markdown to DOCX conversion
# %.docx: %.md
# 	pandoc $^ $(PANDOC_OPTIONS_DOC) -o $@

# Pattern rule to generate TXT files from Python scripts
%.txt: convert_data.py
	python $< $*.md $@

clean:
	rm -f output.pdf $(TEXT_FILES)