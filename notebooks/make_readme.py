"""Jupyter Notebook collection README generator

Copyright 2020 Doug Latornell, 43ravens

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import datetime
import json
import os
from pathlib import Path
import re


nbviewer = "http://nbviewer.jupyter.org/github"
repo = "43ravens/on-notebooks"
repo_dir = "notebooks"
url = f"{nbviewer}/{repo}/blob/master/{repo_dir}"

first_copyright_year = 2020

title_pattern = re.compile("#{1,6} ?")
readme = """The Jupyter Notebooks in this directory are made by
Doug Latornell for sharing of Python code techniques and notes
related to development work on the DFO Ocean Navigator project.

The links below are to static renderings of the notebooks via
[nbviewer.jupyter.org](http://nbviewer.jupyter.org/).
Descriptions below the links are from the first cell of the notebooks
(if that cell contains Markdown or raw text).

"""
for fn in Path(".").glob("*.ipynb"):
    readme += f"* ## [{fn}]({url}/{fn})  \n    \n"
    with open(fn, "rt") as notebook:
        contents = json.load(notebook)
    try:
        first_cell = contents["worksheets"][0]["cells"][0]
    except KeyError:
        first_cell = contents["cells"][0]
    first_cell_type = first_cell["cell_type"]
    if first_cell_type in "markdown raw".split():
        desc_lines = first_cell["source"]
        for line in desc_lines:
            if title_pattern.match(line):
                line = f"{title_pattern.sub('**', line).strip()}**"
            readme += f"    {line}"
        readme += "\n" * 2

this_year = datetime.date.today().year
copyright_years = (
    first_copyright_year
    if this_year == first_copyright_year
    else f"{first_copyright_year}-{this_year}"
)
license = f"""
## License

These notebooks and files are copyright {copyright_years}
by Doug Latornell, 43ravens.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.
"""

with open("README.md", "wt") as f:
    f.writelines(readme)
    f.writelines(license)
