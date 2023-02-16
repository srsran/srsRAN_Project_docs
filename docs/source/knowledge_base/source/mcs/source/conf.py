# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('../../../..'))
 
from docs.source.conf import *


# -- Project information -----------------------------------------------------

project = u'srsRAN Project Knowledge Base - MCS'

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'srsran_project_kb_mcs'


# -- Options for LaTeX output ------------------------------------------------
latex_documents = [
    (master_doc, 'srsran_project_kb_mcs.tex', u'srsRAN Project Knowledge Base - MCS',
     u'SRS', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'srsran_project_kb_mcs.tex', u'srsRAN Project Knowledge Base - MCS',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'srsran_project_kb_mcs.tex', u'srsRAN Project Knowledge Base - MCS',
     author, 'srsran_project_kb_mcs', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']
