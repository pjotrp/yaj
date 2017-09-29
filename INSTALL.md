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

## Install with GNU Guix

Using a recent Guix checkout the tree from https://gitlab.com/genenetwork/guix-bioinformatics. Next install with

    env GUIX_PACKAGE_PATH=./guix-bioinformatics guix package -p ~/opt/yaj -i yaj

this should get you all required dependencies. Load the profile with

    . ~/opt/yaj/etc/profile

so you can see the paths with

    set|grep gnu

Now checkout the journal source code from https://github.com/pjotrp/yaj. You should be able to run the server:

## Run

Configure the server in a JSON file and run it as

    ./run.py ./etc/yaj_config.json

certain settings can be overriden, e.g.,

     env WEB_ASSETS_DIR=../web-assets ./run.py ./etc/yaj_config.json
