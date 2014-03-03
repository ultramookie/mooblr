#!/usr/bin/python

# mooblr
# steve mookie kong
# licensed under gplv3
# http://www.gnu.org/licenses/gpl-3.0.html

import json
import MySQLdb as mdb
import codecs
import urllib2
import oauth2 as oauth

# database stuff populate as necessary
dbuser='DBUSERNAME'
dbpass='DBPASSWORD'
dbhost='localhost'
dbname='mooblr'

# tumblr domain (ie. "ultramookie.tumblr.com")
domain = 'TUMBLRDOMAIN'

# tumblr key (get from http://www.tumblr.com/oauth/apps)
CONSUMER_KEY = "TUMBLRCONSUMERKEY"

# the fields i want
fields = ['id','date','state','title','body','post_url','slug','type']

# the base url
urlbase = 'http://api.tumblr.com/v2/blog/' + domain + '/posts?api_key=' + CONSUMER_KEY

con = mdb.connect(dbhost,dbuser,dbpass,dbname)

url = urlbase
response = urllib2.urlopen(url)
tumblrjson = json.load(response)
tumblrposts = tumblrjson['response']['posts']
for post in tumblrposts:
	if post['type'] == "text" and post['state'] == "published":
		for field in fields:
			if field == 'id':
				tumblrid = post['id']
			if field == 'body' and post.get('body'):
				intext = post['body']
				tumblrtext = intext.encode('ascii','ignore')
			if field == 'body' and not post.get('body'):
				tumblrtext = ''
			if field == 'title' and post.get('title'):
				intext = post['title']
				tumblrtitle = intext.encode('ascii','ignore')
			if field == 'title' and not post.get('title'):
				tumblrtitle = post['slug']
			if field == 'date':
				tumblrdate = post['date'].rsplit(' ',1)[0]
			if field == 'post_url':
				tumblrurl = post['post_url']
			if field == 'slug':
				tumblrslug = post['slug']
		cur = con.cursor()
		sql = u"INSERT IGNORE into mooblr (id,title,text,timestamp,url,slug) VALUES (%s,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (tumblrid,mdb.escape_string(tumblrtitle),mdb.escape_string(tumblrtext),mdb.escape_string(tumblrdate),mdb.escape_string(tumblrurl),mdb.escape_string(tumblrslug))
		cur.execute(sql)
	con.commit()
