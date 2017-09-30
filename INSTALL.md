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

### Install GNU Guix itself

Install GNU Guix using the binary
[install](https://www.gnu.org/software/guix/download/). Follow the
[installation instructions](https://www.gnu.org/software/guix/manual/html_node/Binary-Installation.html)
and make sure you add the key with
[guix archive](https://www.gnu.org/software/guix/manual/html_node/Substitutes.html#Substitutes). Next run a

    guix pull

so guix knows how to find its own package definitions. You should be able to

    guix package -i hello

as a binary package.

### Install journal software with all its dependencies

Using a recent Guix checkout the tree from https://gitlab.com/genenetwork/guix-bioinformatics. Next install with

    env GUIX_PACKAGE_PATH=./guix-bioinformatics guix package -p ~/opt/yaj -i yaj

this should get you all required dependencies. Load the profile with

    . ~/opt/yaj/etc/profile

so you can see the paths with

    set|grep gnu

Now checkout the journal source code from https://github.com/pjotrp/yaj. You should be able to run the server with the following

## Run the webserver

Configure the server in a JSON file and run it as

    ./run.py ./etc/yaj_config.json

certain settings can be overriden, e.g.,

     env WEB_ASSETS_DIR=../web-assets ./run.py ./etc/yaj_config.json
