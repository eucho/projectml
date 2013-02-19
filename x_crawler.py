import urllib2
import time
from BeautifulSoup import BeautifulSoup
import re

def crawl(frm, to):
	opener = urllib2.build_opener()
	site = 'http://acm.timus.ru/'
	uri = 'status.aspx?space=1&from=%s&count=100' % frm
	fw = open('ural.%s_%s'%(frm, to), 'w')
	while frm >= to:
		print frm, to, uri
		req = urllib2.Request(site + uri + '&count=100')
		r = opener.open(req)
		#r = open('300.html', 'r')
		soup = BeautifulSoup(r.read())

		#list columns in need in current page
		list_id = soup.findAll(attrs={'class':'id'})
		list_pid = soup.findAll(attrs={'class':'problem'})
		list_res = soup.findAll(attrs={'class':re.compile('^verdict')})

		#write into file
		list_all = []
		for item in zip(list_id[1:], list_pid[1:], list_res):
			list_all.append(item[0].encodeContents('ascii') + '\t' + \
				item[1].a.encodeContents('ascii')[:4] + '\t' + \
				item[2].encodeContents('ascii') + '\n')
		fw.writelines(list_all)
		fw.flush()

		#find next page
		uri = soup.findAll(text=re.compile('Next'))[-1].parent['href']
		frm = int(uri.split('=')[-1])
	
	fw.close()

if __name__ == '__main__':
	crawl(5000,4500)
