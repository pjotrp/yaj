# Installation

## Dependencies

1. Python
2. Flask
3. [Mako](http://www.makotemplates.org/) for templating
4. Bootstrap

An up-to-date list of dependencies can be found in this GNU Guix
package
[definition](https://gitlab.com/genenetwork/guix-bioinformatics/blob/master/gn/packages/yaj.scm#L69)
that we use for development and deployment.

## Run

Point YAJ_WEB_PATH to JS and CSS assets and run with

    env YAJ_WEB_PATH=~/opt/yaj/share/web ./run.py
