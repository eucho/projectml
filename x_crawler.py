import urllib2
import time
from bs4 import BeautifulSoup
import re
import sys

def crawl(frm, to):
	opener = urllib2.build_opener()
	site = 'http://acm.timus.ru/'
	uri = 'status.aspx?space=1&from=%s' % frm
	fw = open('ural.%s_%s'%(frm, to), 'w')
	while frm >= to:
		print frm, to
		req = urllib2.Request(site + uri + '&count=100')
		while True:
                        try:
                                print uri
                                r = opener.open(req, timeout = 3000)
                                soup = BeautifulSoup(r.read())
                        except:
                                print 'Open failed!'
                        else:
                                break

		#list columns in need in current page
		list_id = soup.find_all(attrs={'class':'id'})
		list_pid = soup.find_all(attrs={'class':'problem'})
		list_coder = [x.a for x in soup.find_all(attrs={'class':'coder'})]
		list_res = soup.find_all(attrs={'class':re.compile('^verdict')})

		#write into file
		list_all = []
		for item in zip(list_id[1:], list_pid[1:], list_coder[1:], list_res):
			list_all.append(item[0].string + u'\t' + \
				item[1].a['href'][-4:] + u'\t' + \
				item[2].string + u'\t' + \
				item[3].string + u'\n')
		fw.writelines([x.encode('utf-8') for x in list_all])
		fw.flush()

		#find next page
		uri = soup.find_all(text=re.compile('Next'))[-1].parent['href']
		frm = int(uri.split('=')[-1])
	
	fw.close()

if __name__ == '__main__':
        try:
                frm = int(sys.argv[1])
                to = int(sys.argv[2])
        except:
                print 'invalid args'
                exit(1)
        crawl(frm, to)
