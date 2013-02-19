from BeautifulSoup import BeautifulSoup
import re
import urllib2

if __name__ == '__main__':
	fw = open('pid_acnt_diffi', 'w')
	opener = urllib2.build_opener()
	site = 'http://acm.timus.ru/'
	uri = 'problemset.aspx?space=1&page=all'
	req = urllib2.Request(site + uri)
	r = opener.open(req)
	soap = BeautifulSoup(r.read())
	l = soap.findAll('a', href=re.compile('^rating'))
	for x in l:
		#get pid
		pid = x['href'].split('=')[-1]

		#get ac count
		cnt = x.string

		#get difficulty
		dif = x.parent.nextSibling.string

		fw.write(pid +'\t'+ cnt +'\t'+ dif + '\n')
	
	fw.close()
