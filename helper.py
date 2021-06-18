from engine.JitObject import JitObject
import os
import argparse
from engine.JitRepository import JitRepository
import sys
from engine.utils import Util


# preparing argparsere
argparser = argparse.ArgumentParser(description= "########## JIT ( A command line tool ######### ")
argsubparsers = argparser.add_subparsers(title= "Commands", dest= "command")
argsubparsers.required = True

argsp = argsubparsers.add_parser("init", help="Initialize a new , empty repository.")
argsp.add_argument("path", metavar="Directory", nargs="?",default= ".", help = "location to create the epository")


argsp = argsubparsers.add_parser("cat-file", help="Provide content of repository objects")
argsp.add_argument("type", metavar="type",
 choices=["blob", "commit", "tag", "tree"],
 help = "Specify the type")

argsp.add_argument("object", metavar="object",
 help="The object to display")
argsp = argsubparsers.add_parser(
    "hash-object",
    help="Compute object ID and optionally creates a blob from a file")

argsp.add_argument("-t",
                   metavar="type",
                   dest="type",
                   choices=["blob", "commit", "tag", "tree"],
                   default="blob",
                   help="Specify the type")

argsp.add_argument("-w",
                   dest="write",
                   action="store_true",
                   help="Actually write the object into the database")

argsp.add_argument("path",
                   help="Read object from <file>")

# main function
def main(argv = sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == "add"   : jit_add(args)
    elif args.command == "cat-file" : jit_cat_file(args)
    elif args.command == "checkout" : jit_checkout(args)
    elif  args.command == "commit"  : jit_commit(args)
    elif args.command == "init"   : jit_init(args)
    elif  args.command == "hash-object"  : jit_hash_object(args)
    elif  args.command == "log"  : jit_log(args)
    elif  args.command == "ls-tree" : jit_ls_tree(args)
    elif args.command == "merge"   : jit_merge(args)
    elif args.command == "rebase"   : jit_rebase(args)
    elif args.command == "tag"   : jit_tag(args)
    elif args.command == "rev-parse"   : jit_rev_parse(args)
    elif args.command == "rm"   : jit_rm(args)
    elif args.command == "show-ref"   : jit_show_ref(args)



def create_repo(path):

    """ create new repository"""
    repo = JitRepository(path, True)
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            print("%s is not a directory!" %path)
            exit()
        if ".jit" in os.listdir(repo.worktree):
            print("Already  a jit repository")
            exit()

    else:
        os.makedirs(repo.worktree)
    

    assert(repo.repo_dir("branches", mkdir = True))
    assert(repo.repo_dir( "refs", "tags", mkdir = True))
    assert(repo.repo_dir("objects", mkdir = True))
    assert(repo.repo_dir("refs", "heads", mkdir = True))

    #.jit/description
    with open(repo.repo_file("description"), "w") as fs:
        fs.write("Unnamed repository; edit this file description to name the repository.\n")
    
    #.git/HEAD
    with open(repo.repo_file("HEAD"), "w") as f:
        f.write("ref: refs/head/master\n")
    
    #config
    with open(repo.repo_file("config"), "w") as f:
        config = repo.repo_default_config()
        config.write(f)
    

		
def jit_init(args):
    create_repo(args.path)



def cat_file(repo, obj, fmt= None):
    jitobject = JitObject(repo)
    sha = jitobject.object_find(obj, fmt= fmt)
    obj = jitobject.object_read(sha)
    sys.stdout.buffer.write(obj.serialize())
def jit_cat_file(args):
    repo = Util.find_repo()
    cat_file(repo, args.object, fmt= args.type.encode())

def object_hash(fd, fmt, repo= None):
    data = fd.read()

    if fmt== b'commit' : obj= JitCommit(repo,data)
    elif fmt == b'tree' :obj = JitTree(repo,data)
    elif fmt == b'tag'  : obj = JitTag(repo,data)
    elif fmt = b'blob'  : obj = GitBlob(repo, data)

    else:
        raise Exception("Unknown type %s!" % fmt)
    
    jitobject = JitObject(repo)
    
    return jitobject.object_write(obj)

def jit_hash_object(args):
    if args.write:
        repo = JitRepository(".")
    else:
        repo = None
    
    with open(args.path, 'rb') as fd:
        sha = object_hash(fd, args.type.encode(), repo)
        print(sha)