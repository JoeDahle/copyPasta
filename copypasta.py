from distutils.dir_util import copy_tree
from time import sleep
#import subprocess
import termios
import sys
import os
import shutil

TERMIOS = termios


def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c


try:
    src = '/media/joe/9016-4EF8/DCIM/'
    dropbox = '/home/joe/Dropbox/CanonPictures/'
    chloe = '/mnt/Chloe/Pictures/'
    copy_tree(src, dropbox)
    print 'copy to dropbox success'
    sleep(0.5)
    try:
        copy_tree(src, chloe)
        print 'copy to HDD \'Chloe\' success'
    except Exception:
        print 'Failed to backup to HDD\nIs the HDD\'Chloe\' mounted at \'mnt\''
    sleep(0.5)
    try:
        print 'Delete the contents of ' + src + ' \'y\' or \'n\''
        deleteMedia = getkey()
        if deleteMedia.lower() == 'y':
            print 'YES'
            print 'Are you sure? ALL CONTENTS WILL BE LOST FOREVER.'
            yesDelete = getkey()
            if yesDelete.lower() == 'y':
                print 'YES, will now delete'
                shutil.rmtree(src)
            else:
                print 'Contents NOT deleted'
        else:
            print 'Contents NOT deleted'
    except Exception:
        print 'failure to delete contents of ', src
except Exception:
    print 'copy failure\nTry again\nIf failure persists, try remounting.'
