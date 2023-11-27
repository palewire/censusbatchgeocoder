"""Configure Sphinx configuration."""
import os
import sys
from datetime import datetime

# Insert the parent directory into the path
sys.path.insert(0, os.path.abspath(".."))

extensions = [
    "myst_parser",
    "sphinx.ext.napoleon",
]
templates_path = ["_templates"]
source_suffix = ".md"
master_doc = "index"

project = "censusbatchgeocoder"
year = datetime.now().year
copyright = f"{year} palewire"

exclude_patterns = ["_build"]

html_theme = "palewire"
html_sidebars = {}
html_theme_options = {
    "canonical_url": f"https://palewi.re/docs/{project}/",
    "nosidebar": True,
}