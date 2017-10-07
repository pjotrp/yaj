We are creating a publish/review/response system where postings are
simply files that can be retrieved from git or IPFS. Similar to an
issue tracker it simply consists of a linked list of files. Initially
this linked list is a JSON file - but later it may be fully handled by
IPFS.

Tasks are defined as:

1. Store postings in the source repo in yaj/doc/issues/ as markdown
files (not a problem since they will be all related to the source code
at this point).
2. Create a list of issues page
3. Display an issue with its linked postings/responses
4. Add a new response (using JSON store)
5. Create interface using IPFS-client
6. Tie it together
