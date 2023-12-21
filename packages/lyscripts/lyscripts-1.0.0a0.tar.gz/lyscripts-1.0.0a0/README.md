<img src="https://raw.githubusercontent.com/rmnldwg/lyscripts/main/github-social-card.png" alt="social card" style="width:830px;"/>

[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/rmnldwg/lyscripts/blob/main/LICENSE)
[![GitHub repo](https://img.shields.io/badge/rmnldwg%2Flymph-grey.svg?style=flat&logo=github)](https://github.com/rmnldwg/lyscripts)
[![build badge](https://github.com/rmnldwg/lyscripts/actions/workflows/build.yml/badge.svg?style=flat)](https://pypi.org/project/lyscripts/)
[![docs badge](https://github.com/rmnldwg/lyscripts/actions/workflows/docs.yml/badge.svg?style=flat)](https://rmnldwg.github.io/lyscripts/)
[![tests badge](https://github.com/rmnldwg/lyscripts/actions/workflows/tests.yml/badge.svg?style=flat)](https://rmnldwg.github.io/lyscripts/)

## What are these `lyscripts`?

This package provides convenient scripts for performing inference and learning regarding the lymphatic spread of head & neck cancer. Essentially, it provides a *command line interface* (CLI) to the [`lymph`](https://github.com/rmnldwg/lymph) library.

We are making these "convenience" scripts public, because doing so is one necessary requirement to making our research easily and fully reproducible. There exists another repository, [`lynference`](https://github.com/rmnldwg/lynference), where we store the pipelines that produce(d) our published results in a persistent way. Head over there to learn more about how to reproduce our work.

## Installation

These scripts can be installed via `pip`:

```bash
pip install lyscripts
```

or installed from source by cloning this repo

```bash
git clone https://github.com/rmnldwg/lyscripts.git
cd lyscripts
pip install .
```

## Usage

After installing the package, run `lyscripts --help` to see the following output:

```
USAGE: lyscripts [-h] [-v]
                 {app,data,evaluate,plot,predict,sample,temp_schedule} ...

Utility for performing common tasks w.r.t. the inference and prediction tasks one
can use the `lymph` package for.

POSITIONAL ARGUMENTS:
  {app,data,evaluate,plot,predict,sample,temp_schedule}
    app                 Module containing scripts to run different `streamlit`
                        applications.
    data                Provide a range of commands related to datasets on
                        patterns of lymphatic progression. Currently, the
                        following modules provide additional commands: 1. The
                        `lyscripts.data.clean` module that converts a LyProX-style
                        table of patient information into a simplified format that
                        is used by the `lymph` model. 2. `lyscripts.data.enhance`,
                        a module for computing consensus diagnoses and to ensure
                        that super- and sublevels are consistently reported. 3.
                        The module `lyscripts.data.generate` for creating
                        synthetic datasets with certain characteristics. 4.
                        Submodule `lyscripts.data.join` to concatenate two
                        datasets, e.g. from different institutions. 5.
                        `lyscripts.data.split`, a module with which datasets may
                        be split into random sets of patient data. The split data
                        may then be used e.g. for cross-validation.
    evaluate            Evaluate the performance of the trained model by computing
                        quantities like the Bayesian information criterion (BIC)
                        or (if thermodynamic integration was performed) the actual
                        evidence (with error) of the model.
    plot                Provide various plotting utilities for displaying results
                        of e.g. the inference or prediction process. At the
                        moment, three subcommands are grouped under
                        `lyscripts.plot`: 1. `lyscripts.plot.corner`, which simply
                        outputs a corner plot with nice labels for a set of drawn
                        samples. 2. The module `lyscripts.plot.histograms` can be
                        used to draw histograms, e.g. the ones over risks and
                        prevalences as computed by the `lyscripts.predict` module.
                        3. Module `lyscripts.plot.thermo_int` allows comparing
                        rounds of thermodynamic integration for different models.
    predict             This module provides functions and scripts to predict the
                        risk of hidden involvement, given observed diagnoses, and
                        prevalences of patterns for diagnostic modalities. The
                        submodules for prediction are currently: 1. The
                        `lyscripts.predict.prevalences` module for computing
                        prevalences of certain involvement patterns that may also
                        be compared to observed prevalences. 2. A module
                        `lyscripts.predict.risks` for predicting the risk of any
                        specific pattern of involvement given any particular
                        diagnosis.
    sample              Learn the spread probabilities of the HMM for lymphatic
                        tumor progression using the preprocessed data as input and
                        MCMC as sampling method. This is the central script
                        performing for our project on modelling lymphatic spread
                        in head & neck cancer. We use it for model comparison via
                        the thermodynamic integration functionality and use the
                        sampled parameter estimates for risk predictions. This
                        risk estimate may in turn some day guide clinicians to
                        make more objective decisions with respect to defining the
                        *elective clinical target volume* (CTV-N) in radiotherapy.
    temp_schedule       Generate inverse temperature schedules for thermodynamic
                        integration using various different methods. Thermodynamic
                        integration is quite sensitive to the specific schedule
                        which is used. I noticed in my models, that within the
                        interval $[0, 0.1]$, the increase in the expected
                        log-likelihood is very steep. Hence, the inverse
                        temparature $\beta$ must be more densely spaced in the
                        beginning. This can be achieved by using a power sequence:
                        Generate $n$ linearly spaced points in the interval $[0,
                        1]$ and then transform each point by computing $\beta_i^k$
                        where $k$ could e.g. be 5.

OPTIONAL ARGUMENTS:
  -h, --help            show this help message and exit
  -v, --version         Display the version of lyscripts (default: False)
```

Each of the individual subcommands provides a help page like this respectively that detail the positional and optional arguments along with their function.
