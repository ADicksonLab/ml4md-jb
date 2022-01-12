# Machine Learning for Molecular Dynamics
## BMB 961 Sec 003 - Spring 2022
This is the course content repository for instructors.  Content on the `main` branch is rendered and distributed to a JupyterBook hosted here: [https://adicksonlab.github.io/ml4md-jb](https://adicksonlab.github.io/ml4md-jb).

## List of instructors:
**Alex Dickson** \
[alexrd@msu.edu](mailto:alexrd@msu.edu)\
Associate Professor, Dept of Biochemistry &amp; Molecular Biology and Dept of Computational Mathematics, Science &amp; Engineering

**Michael Feig** \
[feig@msu.edu](mailto:feig@msu.edu)\
Professor, Dept of Biochemistry &amp; Molecular Biology

## To contribute content:

Clone this git repository to your computer:\
`git clone git@github.com:ADicksonLab/ml4md-jb.git`\
this will create a directory called `ml4md-jb` with all of the source files.

To be able to build and publish the html yourself then you I recommend creating a conda environment:\
`conda create -n jupyterbook`\
`conda activate jupyterbook`

and then installing these packages:\
`pip install jupyter-book`\
`pip install ghp-import`

`jupyter-book` commands begin with `jb` and are used to build the static html (in the `_build` folder).  The `ghp-import` package commits the content of the `_build` folder to a special branch of the repo (`gh_pages`) that hosts the JupyterBook on the github.io site.

## Adding content to the main branch:

To add a lesson, do the following on your terminal:

1) Make sure you are in the main branch:\
   `git checkout main`
2) Make sure the branch is updated:\
   `git pull origin main`
3) Copy the final versions of all of the files you need into that Day's folder (e.g. Day-02)
4) Update the `_toc.yml` file to uncomment out that day's notebooks and update the filenames if they have changed.
5) Add the notebooks and all of their dependent files and commit locally (don't forget `_toc.yml`!):\
   `git add Day-02/Day-02_Fidget_Spinners.ipynb Day-02/fidget_spinner.jpg _toc.yml`
6) Commit your work locally:\
   `git commit -m 'day 2 content'`
7) Push to the remote repository:\
   `git push origin main`
8) Publish to the github.io site:\
   `jb build .`  (use `--all` flag to rebuild all pages when adding new entries)\
   `ghp-import -n -p -f _build/html`\
   or alternatively:\
   `./build_and_deploy.sh`
