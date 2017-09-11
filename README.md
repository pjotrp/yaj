# Yet another Journal

In this repository we are creating a prototype for a novel biomedical
journal for publishing data and analysis resources. This work was
started during the Japan 2017 Biohackathon (September 2017).

## Goals

Key goals the data journal are:

1. Make it easy for researchers to publish data with a short paper
2. Provide a review mechanism
2. Make the paper citeable
3. Provide usable FAIR-data mechanisms

## FAIR

FAIR means the data should be

1. Findable: provide useful metadata
2. Accessible: provide a stable URL
3. Interoperable: use common data formats
4. Reproducible: provide analysis with data (at least as an example)

## Technology and resources


### Git

All versions of papers, review and comments are stored into a public
git repository which means everything can we recovered. We will also
use a database that acts as a cache of git checkouts.

### RDF/OWL

Rather than rolling our own ontologies we'll use whatever is available.

### WikiData and Open Citations

Wikidata/wikicite and open citations have semantic web representations
which can be used to handle citations.

### IPFS

To build in speed and robustness authors are encouraged to host data
on the interplanetary file system (IPFS) which provides download URLs.

### Programming

We opted for Python/flask for the web server. Mostly because Python
has become a lingua franca in bioinformatics and Flask is a well
tested and simple web development framework. For some functionalities
and (perhaps) performance we will use plug-ins which can be written in
any language. The REST API may be written in Elixir.

## Installation

See [INSTALL.md](INSTALL.md).

## Development

For further reading see [development docs](doc/DEVELOPMENT.md)

## License

All code is published under the AGPL. See [LICENSE](LICENSE).

## Copyright

Pjotr Prins, Raoul Bonnal, Francesco Strozzi (C) 2017
