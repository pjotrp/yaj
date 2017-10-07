# Design

# Introduction

# Data blocks

## Publications

Every publication comes as a text file in a supported format (e.g.,
Markdown) accompanied by a metadata file in JSON-LD format. These
publications with metadata are stored in a git repository or
IPFS. Some will be in the source tree (like the 'about' page), but
others may sit anywhere on IPFS.

Metadata is 'named' and stored in directories which act as initial
sections. Information gets cached in a database. The database gets
loaded by an external command (when starting up the service). When
publications/comments get updated both the git repository and database
need to get updated. We assume the database is in sync, though a
regular check should make sure that still holds. The database is never
the authority, i.e., the git repositories are the authority. This
implies that a basic version can run without a database (though it may
miss out on search capabilities and auto-completion).

## Metadata

Metadata is critical for findability and interoperability of data
sources. Linked data and ontologies are established technologies to
achieve just that. Even so, we don't want to impose formal ontologies
on researchers.

The solution is make it easy to create metadata (normally as key-value
pairs). This metadata may be improved over time and grow towards
formal standards. That implies that metadata must be changeable over
time.

Metadata is stored as JSON-LD in a git repository. Simple updates
can be done in the repository.

Schema's for defining fields that may be interesting are
[Project Open Data](https://project-open-data.cio.gov/v1.1/schema/),
[Bioschemas](http://bioschemas.org/).

Linking API's with [Smart-API](http://smart-api.info/website/)

## Links

1. https://steemit.com/
2. wikidata
3. hyper ledger
4. [health care records](https://www.cio.com/article/3171132/innovation/an-ipfs-addressable-storage-model-for-healthcare-with-blockchain.html)
5. http://chriswarbo.net/blog/2017-03-20-web_hosting_with_ipfs_and_nix.html
