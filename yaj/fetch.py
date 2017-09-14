from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE, GIT_SORT_TIME, Repository
from yaj.config import YAJ_GIT

def read(path):
    # repo = Repository(YAJ_GIT)
    # index = repo.index
    # index.read()
    # print(path)
    # id = index[path].id    # from path to object id
    # print(id)
    # for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL|GIT_SORT_TIME):
    #     print(commit.commit_time, ' ', commit.message)
    f = open(path)
    buf = f.read()
    f.close
    return buf
