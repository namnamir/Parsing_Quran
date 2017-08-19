#!/usr/bin/env python
# -*- coding: utf-8 -*-

#for opening links
import urllib2
#for json files
import simplejson
#handeling UTF8 for json files | read more: http://code.opoki.com/loading-utf-8-json-file-in-python/
import codecs

# intitiating the link-style of the pages as well as giving the list of poems
file      = 'Quran.json'
directory = '/home/Quran/'

# opening the json file
def open_file(file):
	with open(file, 'rb') as json_file:
		return(simplejson.load(json_file))

# writing into the json file and close it
def close_file(ayats):
	# using codecs helps to fix the problem of unicode. It write as UTF8 into the json file instead of writing as unicode or unicode-escape
	# read more: http://code.opoki.com/loading-utf-8-json-file-in-python/
	with codecs.open(directory[:-6]+file, 'w', encoding="utf-8") as json_outfile:  
		simplejson.dump(ayats, json_outfile, sort_keys=True, indent=4, ensure_ascii=False)
	json_outfile.close()


#################################################################
# opening the link of each Ayat on Al-Quran and create the json #
#################################################################


# opening the json file into a list
ayats_list = open_file(directory[:-6]+file)

# load all Ayats which is from 1 to 6236
for i in range(1, 6236):
	print "{}\t == Parsing Ayat  ==> {}".format(i,i)

	# geting json from the site
	link_ar = urllib2.urlopen('http://api.alquran.cloud/ayah/'+str(i))
	ayat_ar = simplejson.load(link_ar)
	link_fa = urllib2.urlopen('http://api.alquran.cloud/ayah/'+str(i)+'/fa.fooladvand')
	ayat_fa = simplejson.load(link_fa)
	link_en = urllib2.urlopen('http://api.alquran.cloud/ayah/'+str(i)+'/en.sahih')
	ayat_en = simplejson.load(link_en)

	# downloading the MP3 files
	ogg_ar = urllib2.urlopen('http://cdn.alquran.cloud/media/audio/ayah/ar.parhizgar/'+str(i))
	with open(directory+str(i)+'_ar.ogg','wb') as output:
		output.write(ogg_ar.read())
	ogg_fa = urllib2.urlopen('http://cdn.alquran.cloud/media/audio/ayah/fa.hedayatfarfooladvand/'+str(i))
	with open(directory+str(i)+'_fa.ogg','wb') as output:
		output.write(ogg_fa.read())
	ogg_en = urllib2.urlopen('http://cdn.alquran.cloud/media/audio/ayah/en.walk/'+str(i))
	with open(directory+str(i)+'_en.ogg','wb') as output:
		output.write(ogg_en.read())

	# downloading the PNG file of the Ayat
	png_ar = urllib2.urlopen('http://cdn.alquran.cloud/media/image/'+str(ayat_ar["data"]["surah"]["number"])+'/'+str(ayat_ar["data"]["numberInSurah"]))
	with open(directory+str(i)+'_ar.png','wb') as output:
		output.write(png_ar.read())

	# converting each poem into json by calling get_poem() function which parse the HTML page of each poem
	# English audio by "Ibrahim Walk", Farsi audio by "Fooladvand & Hedayatfar", Arabic audio by Parhizgar
	# English translation by "Saheeh International", Farsi translation by "Mohammad Mahdi Fooladvand"
	ayat = {i:{"Surah_ID":ayat_ar["data"]["surah"]["number"],
			   "Number_of_Ayats":ayat_ar["data"]["surah"]["numberOfAyahs"],
			   "Surah_Name_ar":ayat_ar["data"]["surah"]["name"],
			   "Surah_Name_en":ayat_en["data"]["surah"]["englishName"],
			   "Ayat_in_Surah":ayat_ar["data"]["numberInSurah"],
			   "Juz":ayat_ar["data"]["juz"],
			   "Ayat_Text_ar":ayat_ar["data"]["text"],
			   "Ayat_Text_en":ayat_en["data"]["text"],
			   "Ayat_Text_fa":ayat_fa["data"]["text"],
			   "Ayat_Audio_ar":str(i)+'_ar.ogg',
			   "Ayat_Audio_en":str(i)+'_en.ogg',
			   "Ayat_Audio_fa":str(i)+'_fa.ogg'
			   }}

	# appending each json item into a global list
	ayats_list[0].update(ayat)

print "{} Ayats are loaded into json".format(i)

close_file(ayats_list)
