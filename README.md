Lossless-tools
=======

Some scripts for manipulating your lossless audio collection.

## installation

type this command as root:

    $ make install"
or

    $ prefix=/usr make install

## uninstallation

    $ make uninstall
or
    $ prefix=/usr make uninstall


# apemustdie:

## Description:
    * apemustdie converts .ape files to flac, fixes cuesheets and saves tags.

## Usage:
    * apemustdie DIR
         - converts all ape files in DIR and subdirectories.

## Dependences:
    * python 2.6 or higher
    * mutagen [ aptitude install python-mutagen ]
    * mac [ aptitude install monkeys-audio or emerge media-sound/mac ]

           http://etree.org/shnutils/shntool/support/formats/ape/unix/3.99-u4-b5/mac-3.99-u4-b5.tar.gz

    * flac [ aptitude install flac ]
	

