##############################################################################
# Common make values.
package := frogmouth
run     := poetry run
python  := $(run) python
textual := $(run) textual
lint    := $(run) pylint
mypy    := $(run) mypy
black   := $(run) black
isort   := $(run) isort

##############################################################################
# Methods of running the application.
.PHONY: run
run:				# Run the application
	$(python) -m $(package)

.PHONY: debug
debug:				# Run the application in debug mode
	TEXTUAL=devtools make run

##############################################################################
# Setup/update packages the system requires.
.PHONY: setup
setup:				# Set up the development environment
	poetry install
	$(run) pre-commit install

.PHONY: update
update:			# Update the development environment
	poetry update

##############################################################################
# Package building and distribution.
.PHONY: build
build:				# Build the package for distribution
	poetry build

.PHONY: clean
clean:				# Clean up the package builds
	rm -rf dist

##############################################################################
# Textual tools.
.PHONY: borders
borders:			# Preview the Textual borders
	$(textual) borders

.PHONY: colours
colours:			# Preview the Textual colours
	$(textual) colors

.PHONY: colour colors color
colour: colours
colors: colours
color: colours

.PHONY: console
console:			# Run the textual console
	$(textual) console

.PHONY: diagnose
diagnose:			# Print the Textual diagnosis information
	$(textual) diagnose

.PHONY: easing
easing:			# Preview the Textual easing functions
	$(textual) easing

.PHONY: keys
keys:				# Run the textual keys utility
	$(textual) keys

##############################################################################
# Reformatting tools.
.PHONY: black
black:				# Run black over the code
	$(black) $(package)

.PHONY: isort
isort:				# Run isort over the code
	$(isort) --profile black $(package)

.PHONY: reformat
reformat: isort black		# Run all the formatting tools over the code

##############################################################################
# Checking/testing/linting/etc.
.PHONY: lint
lint:				# Run Pylint over the library
	$(lint) $(package)

.PHONY: typecheck
typecheck:			# Perform static type checks with mypy
	$(mypy) --scripts-are-modules $(package)

.PHONY: stricttypecheck
stricttypecheck:	        # Perform strict static type checks with mypy
	$(mypy) --scripts-are-modules --strict $(package)

.PHONY: checkall
checkall: lint stricttypecheck # Check all the things

##############################################################################
# Utility.
.PHONY: repl
repl:				# Start a Python REPL
	$(python)

.PHONY: shell
shell:				# Create a shell within the virtual environment
	poetry shell

.PHONY: help
help:				# Display this help
	@grep -Eh "^[a-z]+:.+# " $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.+# "}; {printf "%-20s %s\n", $$1, $$2}'

##############################################################################
# Housekeeping tasks.
.PHONY: housekeeping
housekeeping:			# Perform some git housekeeping
	git fsck
	git gc --aggressive
	git remote update --prune
