#!/usr/bin/python
# -*- coding: utf8 -*-

#
# Copyright (C) 2011  Platon Peacel☮ve <https://github.com/lostfound>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from stat import *
from subprocess import *
import mutagen
from mutagen.flac import FLAC
import sys

def get_ext(basename):
	bspl = basename.split('.')
	if len(bspl) > 1:
		ext = bspl[-1]
		return ext.lower()
def print_notice(s):
	print '*'*len(s)
	print s
	print '*'*len(s)

def search_file_by_ext(addr, Ext, recursiv=False):
	subdirs = []
	ape_files = []
	entries = os.listdir(addr)
	for e in entries:
		pth = os.path.join(addr, unicode(e))
		stt = os.stat( pth )
		if S_ISDIR(stt[ST_MODE]):
			subdirs.append(pth)
		elif S_ISREG(stt[ST_MODE]):
			ext = get_ext(os.path.basename(pth))
			if ext == Ext:
				ape_files.append(pth)
	if recursiv:
		for apes in filter(None, map(lambda subdir: search_file_by_ext(subdir, Ext, True), subdirs)):
			ape_files += apes
	return ape_files

def fixCUES(ape):
	addr = os.path.dirname(ape)
	apebn = os.path.basename(ape)
	flac = apebn[:-3] + 'flac'
	cues = search_file_by_ext(addr, 'cue')
	print_notice("checking cuefiles")
	for cuefile in cues:
		do_rewrite = False
		lines = []
		with open(cuefile, "r") as f:
			lines = f.readlines()
			output_lines=[]
			for ln in lines:
				rc = ln.find(apebn)
				if rc >= 0:
					ln = ln[:rc] + flac + ln[rc + len(apebn):]
					do_rewrite = True
				output_lines.append(ln)
		if do_rewrite:
			print_notice('fixing "' + os.path.basename(cuefile) + '"')
			with open(cuefile, "w") as f:
				f.writelines(output_lines)

def _get_tag_prop(tag, keys):
	for k in keys:
		try:
			rc = tag.get(k)
		except:
			continue
		if not rc:
			continue
		try:
			t = type(rc)
			if t in [ mutagen.id3.TPE1
				, mutagen.id3.TIT2
				, mutagen.id3.TALB
				, mutagen.id3.TRCK]:
				rc = rc.text

			elif t in [ mutagen.apev2.APETextValue ]:
				rc = rc[0]
			elif t == mutagen.id3.TDRC:
				try:
					rc = unicode(rc.text[0]) 
				except:
					rc = None
			elif t == list:
				try:
					rc = rc[0]
				except:
					pass
			elif t not in [str, unicode, list]:
				try:
					rc = rc.text
				except:
					try:
						rc = rc[0]
					except:
						continue
				
			if rc and rc != []:
				return rc
		except:
			pass

def APE2FLAC(ape):
	wav = ape[:-3] + 'wav'
	flac = ape[:-3] + 'flac'
	APE_tag = mutagen.File(ape)

	print_notice( "decoding " + os.path.basename(ape))
	rc = Popen([u'mac', ape, wav,'-d']).wait()
	if rc != 0:
		print_notice( "can't decode " + ape )
		sys.exit(1)

	print_notice( "encoding " + os.path.basename(flac) )
	rc = Popen([u'flac', "--best",wav]).wait()
	if rc != 0:
		print "can't encode " + ape
		sys.exit(1)
	try:
		os.remove(ape)
		os.remove(wav)
	except:
		print_notice("Can't remove files")
	fixCUES(ape)

	# Write tags
	if APE_tag.keys():
		artist = _get_tag_prop(APE_tag, [ "artist", '\xa9ART', '\xa9art', 'TPE1' ] )
		album  = _get_tag_prop(APE_tag, [ "album", '\xa9alb', '\xa9ALB', 'TALB' ] )
		title  = _get_tag_prop(APE_tag, [ "title", '\xa9nam', '\xa9NAM', 'TIT2' ] )
		date   = _get_tag_prop(APE_tag, [ "date", '\xa9day', '\xa9DAY', 'TRDC', 'TDRC', "Year", "year" ] )
		trno    = _get_tag_prop(APE_tag, [ "tracknumber", 'trkn', 'TRCK' ] )

		if filter(None, [artist, album, title, date, trno]) == []:
			return
		print_notice( "writing tags" )

		tag = FLAC(flac)
		if artist:
			tag['artist'] = [ artist ]
		if album:
			tag['album'] = [ album ]
		if title:
			tag['title'] = [ title ]
		if date:
			tag['date'] = [ date ]
		if trno:
			tag['tracknumber'] = [ trno ]

		try:
			tag.save()
		except Exception,e:
			print "can not write tags: ", repr(e)
			


def unicode2(s):
	if type(s) == str:
		return unicode(s.decode('utf-8'))
	return s

if len(sys.argv) != 2:
	program_name = os.path.basename(sys.argv[0])
	print "usage: ", program_name , "DIR"
	print len(program_name)*" ", "        converts all ape to flac files in DIR and subdirectories."
	sys.exit()

if __name__ == '__main__':
	ADDR = unicode2(sys.argv[1])
	counter=1
	ape_list=search_file_by_ext(ADDR, 'ape',True)
	total=len(ape_list)
	for x in  ape_list:
		print_notice("Converting apefile " + str(counter) + "/" + str(total))
		counter+=1
		APE2FLAC(x)

		
		

