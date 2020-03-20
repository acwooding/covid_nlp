COVID-19 NLP
==============================

This is an easydata-generated templated intended to help researchers
get up and running quickly with the COVID NLP dataset available from:
    https://pages.semanticscholar.org/coronavirus-research


GETTING STARTED
---------------

* Create and switch to the  virtual environment:
```
cd covid_nlp
make create_environment
conda activate covid_nlp
make update_environment
```


* fetch and process the datasets:

```
make data
```

* Explore the notebooks in the `notebooks` directory. Notebooks
  are numbered to indicate what order they should be run.
=======

Project Organization
------------
* `LICENSE`
* `Makefile`
    * top-level makefile. Type `make` for a list of valid commands
* `README.md`
    * this file
* `catalog`
  * Data catalog. This is where config information such as data sources
    and data transformations are saved
* `data`
    * Data directory. often symlinked to a filesystem with lots of space
    * `data/raw`
        * Raw (immutable) hash-verified downloads
    * `data/interim`
        * Extracted and interim data representations
    * `data/processed`
        * The final, canonical data sets for modeling.
* `docs`
    * A default Sphinx project; see sphinx-doc.org for details
* `notebooks`
    *  Jupyter notebooks. Naming convention is a number (for ordering),
    the creator's initials, and a short `-` delimited description,
    e.g. `1.0-jqp-initial-data-exploration`.
* `environment.yml`
    * (if using conda) The YAML file for reproducing the analysis environment
* `setup.py`
    * Turns contents of `src` into a
    pip-installable python module  (`pip install -e .`) so it can be
    imported in python code
* `src`
    * Source code for use in this project.
    * `src/__init__.py`
        * Makes src a Python module
    * `src/data`
        * Scripts to fetch or generate data. In particular:
        * `src/data/make_dataset.py`
            * Run with `python -m src.data.make_dataset fetch`
            or  `python -m src.data.make_dataset process`
    * `src/analysis`
        * Scripts to turn datasets into output products
    * `src/models`
        * Scripts to train models and then use trained models to make predictions.
        e.g. `predict_model.py`, `train_model.py`

--------

<p><small>This project was built using <a target="_blank" href="https://github.com/hackalog/cookiecutter-easydata">cookiecutter-easydata</a>, an opinionated fork of [cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science) aimed at making your data science workflow reproducible.</small></p>
