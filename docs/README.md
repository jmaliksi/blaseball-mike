# blaseball-mike docs
Docs use [pdoc3](https://pdoc3.github.io/pdoc/) and are built and deployed on merges to `main`. Use triple quotes to add
docstrings to any public method and class or reference a Markdown file in this folder using `.. include:: <file_path>`.

Manual build
1. `pip install pdoc3`
2. `python docs/make_docs.py`