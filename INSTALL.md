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

Configure the server in a JSON file and run it as

    ./run.py ./etc/yaj_config.json

certain settings can be overriden, e.g.,

     env WEB_ASSETS_DIR=../web-assets ./run.py ./etc/yaj_config.json
