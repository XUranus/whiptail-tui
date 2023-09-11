# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'whiptail-tui'
copyright = '2023, XUranus'
author = 'XUranus'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

import os
import sys

# Add the path to your Python code directory
current_dir = os.path.abspath(os.path.dirname(__file__))
# Construct the absolute path to the "whiptailtui" directory
whiptailtui_dir = os.path.join(current_dir, '..', '..')
print(whiptailtui_dir)
sys.path.insert(0, whiptailtui_dir)