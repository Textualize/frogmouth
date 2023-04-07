##############################################################################
# Common make values.
package := textual_markdown_viewer
run     := poetry run
python  := $(run) python
textual := $(run) textual
lint    := $(run) pylint
mypy    := $(run) mypy

##############################################################################
# Methods of running the application.
.PHONY: run
run:				# Run the application.
	$(python) -m $(package)

.PHONY: debug
debug:				# Run the application in debug mode.
	TEXTUAL=devtools TEXTUAL_DEBUG=1 make run

##############################################################################
# Setup/update packages the system requires.
.PHONY: setup
setup:				# Set up the development environment
	poetry install
	$(run) pre-commit install

.PHONY: update
update:			# Update the development environment.
	poetry update

##############################################################################
# Textual tools.
.PHONY: borders
borders:			# Preview the Textual borders.
	$(textual) borders

.PHONY: colours
colours:			# Preview the Textual colours.
	$(textual) colors

.PHONY: colour colors color
colour: colours
colors: colours
color: colours

.PHONY: console
console:			# Run the textual console.
	$(textual) console

.PHONY: diagnose
diagnose:			# Print the Textual diagnosis information.
	$(textual) diagnose

.PHONY: easing
easing:			# Preview the Textual easing functions.
	$(textual) easing

.PHONY: keys
keys:				# Run the textual keys utility.
	$(textual) keys

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
