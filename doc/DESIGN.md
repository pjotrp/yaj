# Design

# Introduction

# Data blocks

## Publications

Every publication comes as a text file in a supported format (e.g.,
Markdown) accompanied by a metadata file in JSON format. These
publications with metadata are stored in a git repository. Some will
be in the source tree (like the 'about' page), but others may sit
anywhere.

Metadata is 'named' and stored in directories which act as initial
sections. Information gets cached in a database. The database gets
loaded by an external command (when starting up the service). When
publications/comments get updated both the git repository and database
need to get updated. We assume the database is in sync, though a
regular check should make sure that still holds. The database is never
the authority, i.e., the git repositories are the authority. This
implies that a basic version can run without a database (though it may
miss out on search capabilities and auto-completion).
