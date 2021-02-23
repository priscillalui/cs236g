#! /usr/bin/env python

from bs4 import BeautifulSoup
import codecs
import os
import subprocess
import zipfile
import pandas as pd
from PIL import Image

dirname = 'rawdata/'
imgdir = 'images/'


if not os.path.exists(dirname):
	os.mkdir(dirname)
	
if not os.path.exists(imgdir):
	os.mkdir(imgdir)
	


def get_surrounding_text(node):
	rtrstr = ""
	leftcount = 8
	rightcount = 8
	last_string_list = []
	for ele in node.previous_elements:
		if ele.name=='img' or ele.name=='hr' or ele.name=='a':
			break
		if ele.string!=None:
			if len(ele.string.split()) > 3:
				if ele.string.split() != last_string_list:
					rtrstr = ele.string + rtrstr
					last_string_list = ele.string.split()
					leftcount = leftcount - 1
				if leftcount==0:
						break
	for ele in node.next_elements:
		if ele.name=='img' or ele.name=='hr' or ele.name=='a':
			break
		if ele.string!=None:
			if len(ele.string.split()) > 3:
				if ele.string.split() != last_string_list:
					rtrstr = rtrstr +  ele.string
					rightcount = rightcount - 1
					last_string_list = ele.string.split()
				if rightcount==0:
					break
	return rtrstr
		


def get_img_nodes(f):
	soup = BeautifulSoup(open(f),'html.parser')
	return soup.find_all('img')


def get_all_txts(imglist):
	''' returns all next text elements of image nodes list'''
	txtlist = []
	for img in imglist:
		txtlist.append(get_surrounding_text(img))
	return txtlist

def get_core(imglist,txtlist,keyword,imageobjects):
	index = 0
	for i in range(len(imglist)):
		img = imglist[i]
		os.system('cp '+dirname+keyword+'-h/'+img.attrs['src']+' '+imgdir)
		#print('Copied image file over to imgdir')
		os.system('mv '+imgdir+img.attrs['src'].split('/')[-1]+' '+imgdir+keyword+'_'+str(index)+'.'+img.attrs['src'].split('.')[-1])
		#print('Renamed image file in imgdir')
		new_filename = keyword+'_'+str(index)+'.'+img.attrs['src'].split('.')[-1]
		img_readpoint = Image.open(os.path.join(imgdir, new_filename))
		#print('Opened image file')
		img_size = img_readpoint.size
		#img_obj = [filename, book, xdim, ydim, text]
		img_obj = [str(os.path.join(imgdir, new_filename)), keyword, img_size[0], img_size[1], txtlist[i]]
		#print('Created img_obj')
		imageobjects.append(img_obj)
		index = index + 1
	return imageobjects


def create_link(keyword):
	return 'https://www.gutenberg.org/files/'+keyword+'/'+keyword+'-h.zip'



def process(keyword, imageobjects):
	#print('About to get image nodes')
	imglist = get_img_nodes(dirname+keyword+'-h/'+keyword+'-h.htm')
	#print('Got image nodes')
	if len(imglist) > 3:
		txtlist = get_all_txts(imglist)
		#print('Got text')
		imageobjects = get_core(imglist,txtlist,keyword,imageobjects)
		#print('Now going to copy')
	else:
		print('TOO FEW (<3) IMAGES!')
	return imageobjects
	

def download_and_extract(keyword, imageobjects):
	#os.system('wget '+create_link(keyword))
	#os.system('mv '+keyword+'-h.zip '+dirname)
	#zipref = zipfile.ZipFile(dirname+keyword+'-h.zip')
	#zipref.extractall(dirname)
	#zipref.close()

	#os.system('rm '+'rawdata/'+keyword+'-h.zip')

	imageobjects = process(keyword, imageobjects)

	return imageobjects


#Children's Picture Books - 179
#list1 = [22755, 20404, 22818, 17782, 19361, 25433, 24692, 10737, 13646, 20860, 22201, 23765, 23350, 11592, 12227, 19722, 10749, 18341, 22887, 22055, 23483, 22921, 17060, 20181, 18546, 19772, 11979, 23302, 24610,  23479, 17102, 23652, 24795, 21884, 18360, 19991, 14077, 20437, 20579, 15661, 21428, 13035, 18417, 11098, 22335, 24644, 19177, 12109, 19197, 10469, 10557, 20693, 17824, 20723, 24849, 18735, 10754, 22896, 13648, 23462, 23794, 24778, 13650, 20113, 



list1 = ['14838','15284','14407','14868','14814','14837','15284','14872','14304','45264','14220','15137','19805','17089','15575','15077','14848','14877','14797','45265','15234','23350','46','120','236','421','460','501','1033','1154','1430','1867','5347','5601','7425','8574','8995','9075','9383','10142','10436','11171','11757','11860','12630','13355','14220','14304','14375','14407','14732','14797','14814','14837','14848','14868','14872','15077','15168','15234','15284','15521','15575','15976','16259','16686','17089','17250','18614','19002','19089','19092','19337','19722','19805','19859','20606','20781','20877','20997','21015','21914','21935','21994','23661','23869','23871','24022','24053','24286','24430','24459','24772','25496','25519','25564','25581','25609','25610','25611','25617','45264','45265']

list2 = ['17824','11162','21884','20579','11095','15661','10469','10557','20652','18155','18343','22406','13035','19361','18341','18360','19991','14077','18417','19177','12109','19868','10634','20777','18596','14081','23462','11979','23302','17283', '17282','25432','25418','25433','23479','20437','23521','18344','18546','19772','23452','23344','23765','20693','17102','17117','15809','19541','23794','22282','17168','22818','23433','23749','19197','11936','19915','12116','20656','17782','18937','13646','13648','13650','20113','14184','20748','10737','14110','17135','17382','22181','20404','14230','24912','20181','20860','22201','23665','10742','17060','19722','18742','22420']

list3 = ['22755','16081','11065','19169','12227','11592','24692','10749','22887','22055','23483','22921','24894','23652','24795','10979','11023','21428','11098','22335','24644','10834','11092','11073','20723','20511','24849','18735','10754','22896','11877','17162','17163','20575','24778','20017','24694','24736','24738','22778','22891','15621','22561','23322','23407','23336','24734','22529','11241','24834','10965','10983','24609','24610','19537','19531','19366','10607','20511','23794','5312','4901','18546','24623','17208','18742','24475','24476','24477','24478','24479','24938','24939','24940','24941','24942','24943','14170','14335','19821','16552','16524','28129','28130','28131','28132','28133','28134','28135','28136','28137','28138','28139','28140','28141','28142','28143','15928','14493','17536','40752','40753','40754','40755','40756','40757','42156','42157','42158','42159','42160','42161','42162','21047','24474']

keywordslist = list1 + list2 + list3
keywordslist  =list(set(keywordslist))
print(len(keywordslist))
print()

imageobjects = []
failed_books = []

for keyword in keywordslist:
	#print('Trying book '+str(keyword)+'...')
	try:
		imageobjects = download_and_extract(keyword, imageobjects)
	except:
		failed_books.append(keyword)
		input("Please press enter....")
		print()
		print()
		print()

print("IDs of books that failed: ")
print(failed_books)

columns = ['filename','book','xdim','ydim','text']
df = pd.DataFrame(imageobjects, columns =columns)
df.to_csv('images2.csv')

#22 books failed:
# 23322, 10142, 12227, 20860, 16259, 15661, 5312, 20997, 24286,  24894, 7425, 42162, 15976, 9075, 23479, 23665, 17382, 24644, 42156, 8995, 25432, 120 - Couldn't get image nodes
# 11073 - got first 4 images