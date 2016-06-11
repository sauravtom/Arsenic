

import wikipedia
import os
import pyvona
import re
import sys
import string
import time
start_time = time.time()

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
NUMBER_OF_IMAGES = 5

FONT_LOC = '%s/design_assets/impact.ttf'%DIR_PATH

UNDERCOLOR = 'rgba(0,0,0)'
FILLCOLOR = 'rgba(251,251,255)'

v = pyvona.create_voice('GDNAJJ2TZFHSNAJAEYHA', 'vOgSfcz88uZxElIU2K5PLAgWfIJiajojTg81Wla1')

def clean(text):
    text = text.strip()
    text = filter(lambda x: x in string.printable, text)
    #text.encode('ascii', 'ignore')
    text.encode('ascii',errors='ignore')
    text = text.replace('"','')
    text = text.replace("'","")
    return text

def summarize(text):
	text = text.split('.')
	text = ".".join(text)
	#remove text in round brackets and square brackets
	text = re.sub(r'\([^)]*\)', '', text)
	text = re.sub(r'\[[^)]*\]', '', text)
	text = text[:1050]
	text = text.replace('\n','')
	return text

def bake(page_name,summary):
	summary_list = summary.split('.')
	for counter in range(NUMBER_OF_IMAGES+1):
		try:
			title = summary_list[counter]
			if len(title) > 130:
				title = title[:125] + '...'
			if len(title) < len(page_name):
				title = ""
		except:
			title = page_name
		
		title = clean(title)
		title = title.replace("=","")
		title=title.upper()

		#normalize the dimensions of the png files
		os.system("convert %s/oven/temp/slide_%s.png \( -clone 0 -blur 0x15 -resize 480x480\! \) \( -clone 0 -resize 480x480 \) -delete 0 \
		    -gravity center -compose over -composite %s/oven/temp/slide_%s.png"%(DIR_PATH,counter,DIR_PATH,counter))


		#os.system("convert -size %sx%s -stroke '%s' -strokewidth 2 -font %s \
        #        -fill '%s' -gravity center -background transparent \
        #        caption:'%s' -flatten %s/oven/temp/caption_%s.png"%(480,480/3+40,UNDERCOLOR,FONT_LOC,FILLCOLOR,title.upper(),DIR_PATH,counter))

		cmd= '''
		convert -background '#0008' -fill white -gravity west -size 480x180 -font %s caption:"%s"  %s/oven/temp/slide_%s.png +swap -gravity south -composite  %s/oven/temp/slide_%s.png
		'''%(FONT_LOC,title,DIR_PATH,counter,DIR_PATH,counter)
		os.system(cmd)

		#adding captions to slides
		#os.system("composite -gravity South %s/oven/temp/caption_%s.png %s/oven/temp/slide_%s.png %s/oven/temp/slide_%s.png"%(DIR_PATH,counter,DIR_PATH,counter,DIR_PATH,counter))

	# os.system("ffmpeg -i %s/oven/temp/slide_%%d.png -vcodec mpeg4 %s/oven/temp/video_fast.mp4"%(DIR_PATH,DIR_PATH))
	# os.system('ffmpeg -i %s/oven/temp/video_fast.mp4 -vf "setpts=(150)*PTS" %s/oven/temp/final_output.mp4'%(DIR_PATH,DIR_PATH))

	#add narration to video
	#os.system("ffmpeg -i %s/oven/temp/final_output.mp4 -i %s/oven/temp/narration.mp3 \
    #    %s/oven/temp/0final.mp4"%(DIR_PATH,DIR_PATH,DIR_PATH))

		
def download_images(query,number='6'):
	os.system('node %s/download_images.js "%s" %s'%(DIR_PATH,query,number))

def generate_voice(text='hello world'):
	v.codec = 'mp3'
	v.voice_name = 'Raveena'
	v.fetch_voice(text, '%s/oven/temp/narration'%(DIR_PATH))


def main(query='New York'):
	os.system('mkdir %s/oven/temp/'%(DIR_PATH))
	page_name = wikipedia.search(query, results=1)

	try:
		result = wikipedia.page(page_name[0])
	except wikipedia.exceptions.DisambiguationError as e:
		result = wikipedia.page(e.options[0])

	text = result.content
	summary = summarize(text)

	download_images(query,NUMBER_OF_IMAGES)
	print "Generating Voice Now"
	generate_voice(summary)
	#bake the oven
	bake(page_name[0],summary)

	folder_name = query.replace(" ",'_')
	folder_name = folder_name.lower()
	folder_name = folder_name.strip()
	os.system("mv %s/oven/temp %s/oven/%s"%(DIR_PATH,DIR_PATH,folder_name))

def big_short():
	term_list = 'isro,pakistan,supertech,obama,arvind_kejriwal,carcinogen,bread,noida,monsoon,IPL,India'
	for term in term_list.split(','):
		main(term)


if __name__ == '__main__':
	big_short()
	'''
	subdirectories = os.listdir('%s/oven/'%(DIR_PATH))
	query = sys.argv[1]
	if query in subdirectories:
		pass
		# os.system("rm -rf %s/oven/%s"%(DIR_PATH,query))
		# main(query)
	else:
		main(query)
	print int((time.time() - start_time)/60)
	'''


