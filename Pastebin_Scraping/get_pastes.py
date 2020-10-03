
# Pastebin Pro account scraper
import requests
import json
import constants
import asyncio

paste_url_keys=[] 
paste_url_users=[]
keywords = []

def get_250_pastes():
	url = "https://scrape.pastebin.com/api_scraping.php?limit=250"
	s = requests.Session()
	result = s.get(url)
	keys_list = []
	users_list = []
	pastes_with_title=[]
	for each in json.loads(result.text):
		keys_list.append(each["key"])
		if each["user"]:
			users_list.append(each["user"])
		if each["title"]:
			pastes_with_title.append((each["title"],each["key"]))
	save_keys_to_file(keys_list)
	save_users_to_file(users_list)
	save_titles_keys_file(pastes_with_title)



# load keys from keys file to keys list. this keys list avoids redundancies
def load_keys_to_list():
	filename = constants.DIR_PATH+constants.FILENAME_KEYS+constants.FILENAME_EXT
	with open(filename,'r') as fname:
		for line in fname:
			key = line.strip()
			paste_url_keys.append(key)

# load users from users file to users list. this users list avoids redundancies
def load_users_to_list():
	filename = constants.DIR_PATH+constants.FILENAME_USERS+constants.FILENAME_EXT
	with open(filename,'r') as fname:
		for line in fname:
			user = line.strip()
			paste_url_users.append(user)

# save all keys to a keys file
def save_keys_to_file(keys):
	filename = constants.DIR_PATH+constants.FILENAME_KEYS+constants.FILENAME_EXT
	with open(filename,'a+') as fname:
		for each in keys:
			if(each not in paste_url_keys):
				fname.write(each+"\n")
	#load newly appended keys to key list
	load_keys_to_list() 

# save all users to a users file
def save_users_to_file(users):
	filename = constants.DIR_PATH+constants.FILENAME_USERS+constants.FILENAME_EXT
	with open(filename,'a+') as fname:
		for each in users:
			if(each not in paste_url_users):
				fname.write(each+"\n")
	#load newly appended keys to key list
	load_users_to_list()

# save pastes with titles to this file
def save_titles_keys_file(titles_keys):
	filename = constants.DIR_PATH+constants.FILENAME_PASTES_WITH_TITLE+constants.FILENAME_EXT
	with open(filename,'a+') as fname:
		for each in titles_keys:
			fname.write("Title : "+each[0]+" https://pastebin.com/"+each[1]+"\n")

#scrapes each paste and checks ifts important by checking for keyword in the paste body
async def scrape_urls_for_keyword():
	important_pastes =[]
	load_keywords()
	scrape_url = "https://scrape.pastebin.com/api_scrape_item.php?i="
	s = requests.Session()
	for each in paste_url_keys:
		res = s.get(scrape_url+each)
		for keyword in keywords:
			if(keyword in res.text):
				important_pastes.append((keyword,each))
	write_imp_pastes_to_file(important_pastes)

# loads keywords from file to keylist
def load_keywords():
	filename = constants.DIR_PATH+constants.FILENAME_KEYWORDS+constants.FILENAME_EXT
	with open(filename, 'r') as fname:
		for line in fname:
			keyword = line.strip()
			keywords.append(keyword)

# Write all important pastes where keywords were found in a file
def write_imp_pastes_to_file(imp_list):
	filename = constants.DIR_PATH+constants.FILENAME_IMP_PASTES+constants.FILENAME_EXT
	with open(filename, 'a+') as fname:
		for each in imp_list:
			fname.write(each[0]+" : "+"https://pastebin.com/"+each[1]+"\n")

if __name__ == '__main__':
	# get previous values to avoid redundant already crawled pastes
	load_keys_to_list()
	load_users_to_list()
	get_250_pastes()
	asyncio.run(scrape_urls_for_keyword())















