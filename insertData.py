#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

#root_dir = "/home/tusion/Downloads"
root_dir = "/home/tusion/Work/Android/android_source"

total_count = 0
file_count = 0
dir_count = 0

#*****************************************************
# list all directory and files 
# check file: 
# ls /home/tusion/Downloads -lR | grep "^-" | wc -l
# check dir:
# ls /home/tusion/Downloads -lR | grep "^d" | wc -l
def listDir( root_dir, cursor ):
	global file_count
	global dir_count
	global total_count

	for lists in os.listdir( root_dir ):
		path = os.path.join( root_dir, lists)
		if ( os.path.isdir(path) ):
			#print '[d]: ' + lists+", " + path
			dir_sql =""" INSERT INTO dir_string_tb(\
			id, type, file, path, last_update)\
			VALUES(NULL, 0, "%s","%s", now())"""%(lists,path)

			#print dir_sql
			executeDB(cursor, dir_sql )
			dir_count += 1
			total_count += 1
			print 'total: %d, dir: %d, file:%d'%\
					(total_count, dir_count, file_count )
			listDir( path, cursor)

		else:
			#print '[f]: ' + lists+", " + path
			file_sql = """INSERT INTO dir_string_tb(\
			id, type, file, path, last_update)\
			VALUES(NULL, 1, "%s","%s", now())"""%(lists,path)
						
			#print file_sql
			executeDB( cursor, file_sql )
			file_count += 1
			total_count += 1
			print 'total: %d, dir: %d, file:%d'%\
					(total_count, dir_count, file_count )
	return [dir_count, file_count]
			

#***************************************************
def executeDB( cursor, sql ):
	try:
		cursor.execute( sql )
	except db.error, e:
		print e

#***************************************************
# main
print '-'*60
print 'list dir: ' + root_dir
print ''

try:
	db = MySQLdb.connect(
		host = 'localhost',
		user = 'root',
		passwd = 'root',
		db = 'hash_test_db',
		charset = 'utf8')
	db.autocommit( True )
	
except Exception,e:
	print e

cursor = db.cursor()

sql ="drop table if exists dir_string_tb"
executeDB( cursor, sql );

sql = '''
		create table dir_string_tb
		(
			id	int unsigned not null auto_increment primary key,
			type	TINYINT(1) NOT NULL,
			file	VARCHAR(128) CHARACTER SET utf8 NOT NULL,
			path	VARCHAR(255) CHARACTER SET utf8 NOT NULL,
			last_update timestamp not null
		)
	'''
executeDB( cursor, sql )


timestamp_1 = time.clock()

(dir_count, file_count) = listDir( root_dir,cursor)

timestamp_2 = time.clock()
time_elapsed = timestamp_2 - timestamp_1

print '-'*60
print 'Total dir number:' + str( dir_count ) +\
		', file number: ' + str( file_count )
print 'time elapsed: ' + str(time_elapsed) + ' s'
