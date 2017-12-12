# -*- coding: utf-8 -*-

import sys
import os
import re
import subprocess

import sphinx_rtd_theme

# Allow import/extensions from current path
sys.path.insert(0, os.path.abspath('.'))
from definitions import acronyms     # This includes things like |HRTF|
from definitions import latexmacros  # Math definitions like \x


# -- GENERAL -------------------------------------------------------------

project = 'Sound Field Synthesis Toolbox'
copyright = '2016-2017, SFS Toolbox Developers'
author = 'SFS Toolbox Developers'

needs_sphinx = '1.3'  # minimal sphinx version
extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.viewcode',
        'sphinxcontrib.katex',  # Modified version to include clickable eq numbers and
                    # avoid the ugly looking standard result. There is also
                    # a pull request for this:
                    # https://github.com/rtfd/sphinx_rtd_theme/pull/383
        #'sphinx.ext.mathjax',
        'matplotlib.sphinxext.plot_directive',
        'sphinxcontrib.bibtex'
]
master_doc = 'index'
source_suffix = '.rst'
exclude_patterns = ['_build']
# The full version, including alpha/beta/rc tags.
#release = version
try:
    release = subprocess.check_output(
            ('git', 'describe', '--tags', '--always', '--abbrev=0'))
    release = release.decode().strip()
    release = '(v' + release.rsplit('.')[-1] + ')'  # 1.0.3 -> (v3)
except Exception:
    release = '<unknown>'


# -- FIGURES AND CODE ----------------------------------------------------

# Enable numbering of figures and tables
numfig = True
math_numfig = True
# Plot settings for matplot
plot_include_source = True
plot_html_show_source_link = False
plot_html_show_formats = False
plot_formats = ['png', 'pdf']
plot_pre_code = '''
import numpy as np
from matplotlib import pyplot as plt
import sfs
plt.rcParams['figure.figsize'] = 8, 4.5  # inch
def save_fig(file_name):
    dpi = 80
    plt.savefig(file_name + '.png', dpi=dpi)
    plt.savefig(file_name + '.pdf', dpi=dpi)
'''

# Code syntax highlighting style
pygments_style = 'trac'


# -- ACRONYMS AND MATH ---------------------------------------------------

def latex_to_katex(macros):
    "Converts LaTeX \def statements to KaTeX macros"
    # Remove empty lines
    macros = macros.strip()
    tmp = []
    for line in macros.splitlines():
        # Remove spaces from every line
        line = line.strip()
        # Remove "\def" at the beginning of line
        line = re.sub(r'^\\def[ ]?', '', line)
        # Remove parameter before {} command definition
        line = re.sub(r'(#[0-9])+', '', line, 1)
        # Remove outer {} command brackets with ""
        line = re.sub(r'( {)|(}$)', '"', line)
        # Add "": to the new command
        line = re.sub(r'(^\\[A-Za-z]+)', r'"\1":', line, 1)
        # Add , at end of line
        line = re.sub(r'$', ',', line, 1)
        # Duplicate all \
        line = re.sub(r'\\', r'\\\\', line)
        tmp.append(line)
    macros = '\n'.join(tmp)
    return macros


# Append acronyms at the end of every pag
rst_epilog = acronyms

katex_macros = latex_to_katex(latexmacros)


# -- HTML ----------------------------------------------------------------

def setup(app):
    """Include custom theme files to sphinx HTML header"""
    app.add_stylesheet('css/abbr.css')
    app.add_stylesheet('css/math.css')

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {'display_version': True}
html_title = "SFS Toolbox"
html_short_title = ""
htmlhelp_basename = 'sfs-doc'


# -- LATEX ---------------------------------------------------------------

latexmacros += r'''
\makeatletter
\ltx@ifundefined{fancyhf}{}{
  % Use \pagestyle{normal} as the primary pagestyle for text.
  \fancypagestyle{normal}{
    \fancyhf{}
% (for \py@HeaderFamily cf "TITLES")
    \fancyfoot[LE,RO]{{\py@HeaderFamily\thepage}}
    \fancyfoot[LO]{{\py@HeaderFamily\nouppercase{\rightmark}}}
    \fancyfoot[RE]{{\py@HeaderFamily\nouppercase{\leftmark}}}
    \fancyhead[LE,RO]{{\py@HeaderFamily
    \href{http://sfstoolbox.org/}{\color{black}http://sfstoolbox.org/} \hfill \py@release}}
    \renewcommand{\headrulewidth}{0.4pt}
    \renewcommand{\footrulewidth}{0.4pt}
    % define chaptermark with \@chappos when \@chappos is available for Japanese
    \ltx@ifundefined{@chappos}{}
      {\def\chaptermark##1{\markboth{\@chapapp\space\thechapter\space\@chappos\space ##1}{}}}
  }
  % Update the plain style so we get the page number & footer line,
  % but not a chapter or section title.  This is to keep the first
  % page of a chapter and the blank page between chapters `clean.'
  \fancypagestyle{plain}{
    \fancyhf{}
    \fancyfoot[LE,RO]{{\py@HeaderFamily\thepage}}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0.4pt}
  }
}
\makeatother
'''

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'preamble': latexmacros,  # command definitions
    'figure_align': 'htbp',
    'sphinxsetup': 'TitleColor={rgb}{0,0,0}, verbatimwithframe=false, VerbatimColor={rgb}{.96,.96,.96}',
    'releasename': '\href{https://doi.org/10.5281/zenodo.1112452}{\color{black}doi:10.5281/zenodo.1112452}',
}
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass, toctree_only).
latex_documents = [
    (master_doc,
     'sfs-toolbox-documentation.tex',
     u'Theory of Sound Field Synthesis',
     u'SFS Toolbox Developers',
     'manual',
     True),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = 'img/header.png'
