FROM quay.io/jupyter/scipy-notebook:python-3.11

USER root

RUN apt-get update
RUN apt-get -y  install openjdk-11-jdk

USER ${NB_UID}

RUN pip install pyppeteer
RUN pyppeteer-install

RUN conda install -y -q -c conda-forge pydot python-graphviz

RUN pip install pycsp3


WORKDIR "${HOME}"
