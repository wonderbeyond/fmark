#!/usr/bin/python
# coding=utf-8

import os, sys, argparse
import gdbm as dbm

DB_FILE = os.path.expanduser('~/.fmarks')
EDITOR = 'vim'

parser = argparse.ArgumentParser(description='mark or fetch a file with shortname')

# global arguments
parser.add_argument('--dbfile', default=DB_FILE)

subcmds = parser.add_subparsers(help='sub-command help')

# command add
cmd_add = subcmds.add_parser('add', help='add new file mark')
cmd_add.add_argument('mark', action='store')
cmd_add.add_argument('filename', action='store')

# command get
cmd_get = subcmds.add_parser('get', help='get the file by mark')
cmd_get.add_argument('mark', action='store')
cmd_get.add_argument('-e', '--edit', action='store_true')
cmd_get.add_argument('--editor', default=EDITOR)

# command_del
cmd_del = subcmds.add_parser('del', help='del a mark')
cmd_del.add_argument('mark', action='store')

# command list
cmd_ls = subcmds.add_parser('ls', help='ls all marks')
cmd_ls.add_argument('-l', '--long', action='store_true')


args = parser.parse_args()

# open mark database
mark_db = dbm.open(args.dbfile, 'c')

if 'add' in sys.argv:
    filename = os.path.realpath(args.filename)
    print 'mark `%s` as %s' % (filename, args.mark)
    mark_db[args.mark] = filename
elif 'get' in sys.argv:
    try:
        filename = mark_db[args.mark]
        #print '%s hit %s' % (args.mark, filename)
        if not args.edit:
            print filename
        else:
            os.system('%s %s' % (args.editor, filename))
    except KeyError:
        print 'no `%s`' % args.mark
        pass
elif 'del' in sys.argv:
    print 'del mark: %s' % args.mark
    try:
        del mark_db[args.mark]
    except:
        pass
elif 'ls' in sys.argv:
    if args.long:
        for key in mark_db.keys():
            print '%s -> %s' % (key, mark_db[key])
    else:
        for m in mark_db.keys(): print m
