from genericpath import exists
import os
import argparse
import collections
from engine.JitRepository import JitRepository
import hashlib
import re
import sys
import zlib


# preparing argparsere
argparser = argparse.ArgumentParser(description= "########## JIT ( A command line tool ######### ")
argsubparsers = argparser.add_subparsers(title= "Commands", dest= "command")
argsubparsers.required = True

argsp = argsubparsers.add_parser("init", help="Initialize a new , empty repository.")
argsp.add_argument("path", metavar="Directory", nargs="?",default= ".", help = "location to create the epository")



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
