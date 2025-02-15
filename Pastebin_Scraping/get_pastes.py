
# Pastebin Pro account scraper 
# Author himakiran@gmail.com
# This program scrapes pastebin posts using the official pastebin API


import requests
import json
import constants
import asyncio
import webbrowser
import textwrap
from tqdm import tqdm

paste_url_keys = set([])
paste_url_users = set([])
titles_and_keys = []
keywords  = []

def get_250_pastes():
	"""
	Get the maximum pastes allowed by pastebin official api
	"""
	#print("Entering get_250_pastes \n")
	url = "https://scrape.pastebin.com/api_scraping.php?limit=250"
	s = requests.Session()
	result = s.get(url)
	try:
		for each in json.loads(result.text):
			
			try:
				
				paste_url_keys.add(each['key'])
				if each['title']:
					titles_and_keys.append((each['title'],each['key']))
				else:
					titles_and_keys.append(('',each['key']))
				
			except Exception as e:
				print("unable to add key : "+each['key']+" Exception : " + str(e))
				continue
			if each["user"]:
				try:
					paste_url_users.add(each["user"])
					
				except:
					print("unable to add user : "+each["user"])
					continue
		#print("After scraping Keys : " + str(paste_url_keys))	
		#print("After scraping Users : "+ str(paste_url_users))
		#print("After scraping Titles and Keys : "+ str(titles_and_keys))
		save_keys_to_file(paste_url_keys)
		save_users_to_file(paste_url_users)
		save_pastes(titles_and_keys)
		#print("Exiting get_250_pastes \n")
	except Exception as e:
		print(" Whitelist your IP or : "+" Exception : " + str(e))
	



def load_keys_to_list():
	"""
	load keys from keys file to keys set to avoid redundancy
	"""
	#print("Entering load_keys_to_list \n")
	filename = constants.DIR_PATH+constants.FILENAME_KEYS+constants.FILENAME_EXT
	with open(filename,'r') as fname:
		for line in fname:
			key = line.strip()
			try:
				paste_url_keys.add(key)
			except:
				continue
	#print("Existing keys : "+str(paste_url_keys))
	#print("Exiting load_keys_to_list\n")
	
	


def load_users_to_list():
	"""
	load users from users file to users set to avoid redundancy
	"""
	#print("Entering load_users_to_set\n")
	filename = constants.DIR_PATH+constants.FILENAME_USERS+constants.FILENAME_EXT
	with open(filename,'r') as fname:
		for line in fname:
			user = line.strip()
			try:
				paste_url_users.add(user)
			except:
				continue
	#print("Existing users : "+str(paste_url_users))
	#print("Exiting load_users_to_set\n")
	
	

def save_keys_to_file(keys):
	"""
	save all scraped keys without duplicates to the keys file

	Parameters:
    keys (set): All previously and presently scraped keys set.
	"""
	#print("Entering save_keys_to_file\n")
	filename = constants.DIR_PATH+constants.FILENAME_KEYS+constants.FILENAME_EXT
	with open(filename,'w+') as fname:
		for each in keys:
			fname.write(each+"\n")
	#print("Exiting save_keys_to_file\n")


def save_users_to_file(users):
	"""
	save all scraped users without duplicates to the users file

	Parameters:
    users (set): All previously and presently scraped keys set.
	"""
	#print("Entering save_users_to_file\n")
	filename = constants.DIR_PATH+constants.FILENAME_USERS+constants.FILENAME_EXT
	with open(filename,'w+') as fname:
		for each in users:
			fname.write(each+"\n")
	#print("Exiting save_users_to_file\n")


def save_pastes(titles_and_keys):
	"""
	save all pastes with first 10 lines of body to a file

	Parameters:
    titles_and_keys (list): A list of tuples consisting of title and key of each post

	"""
	#print("Entering save_pastes \n")
	url = "https://scrape.pastebin.com/api_scrape_item.php?i="
	s = requests.Session()
	filename = constants.DIR_PATH+constants.FILENAME_PASTES+constants.FILENAME_EXT
	with open(filename,'w+') as fname:
		print("\n\tSaving pastes in pastes.txt ...\n")
		for each in tqdm(titles_and_keys):
			title,key = each
			fname.write("\n================================================================================================\n")
			fname.write(" Title : "+title+"\n")
			fname.write(" URL : https://pastebin.com/"+key+"\n")
			paste = s.get(url+key)
			lines = textwrap.wrap(paste.text, width=50)
			try:
				for i in range(10):
					fname.write(lines[i])
			except:
				fname.write("Complete...")
			fname.write("\n================================================================================================\n")
	#print("Exiting save_pastes\n")

def load_keywords():
	"""
	loads keywords from file to keylist
	"""
	#print("Entering load_keywords\n")
	filename = constants.DIR_PATH+constants.FILENAME_KEYWORDS+constants.FILENAME_EXT
	with open(filename, 'r') as fname:
		for line in fname:
			keyword = line.strip()
			keywords.append(keyword)
	
	#print("Exiting load_keywords\n")


async def scrape_urls_for_keyword():
	"""
	scrapes each paste and checks for keyword in the paste body

	"""
	#print("Entering scrape_urls_for_keyword\n")
	print("\n\tscraping pastes for keywords ... \n")
	important_pastes =[]
	load_keywords()
	for each in tqdm(paste_url_keys):
		url = "https://scrape.pastebin.com/api_scrape_item.php?i="
		s = requests.Session()
		paste = s.get(url+each)
		lines = textwrap.wrap(paste.text, width=50)
		for keyword in keywords:
			for line in lines:
				if(keyword in line):
					important_pastes.append((keyword,each))
					break
	write_imp_pastes_to_file(important_pastes)
	#print("Exiting scrape_urls_for_keyword\n")




def write_imp_pastes_to_file(imp_list):
	"""
	Write all important pastes where keywords were found in a file
	Parameters:
    imp_list (list): A list of tuples each of which contains the keyword and the paste key
	"""
	new_keys_list = []
	#print("Entering write_imp_pastes_to_file\n")
	filename = constants.DIR_PATH+constants.FILENAME_IMP_PASTES+constants.FILENAME_EXT
	with open(filename, 'w') as fname:
		for each in imp_list:
			fname.write(each[0]+" : "+"https://pastebin.com/"+each[1]+"\n")
			new_keys_list.append(each[1])

	# ask user if he wants to see the pastes now
	if input('Do You Want To See the pastes now ? [y/n]') != 'y':
		quit()
	else:
		open_imp_urls_in_tabs(new_keys_list)
	#print("Exiting write_imp_pastes_to_file\n")

def open_imp_urls_in_tabs(list_of_paste_urls):
	"""
	Opens the important urls in the default web browser limited to selected
	no of tabs as decided by constants.NO_OF_TABS_AT_A_TIME
	Parameters:
    list_of_paste_urls (list): list of paste keys deemed important
    """
	len_list = len(list_of_paste_urls)
	i = 1
	while i <= len_list:
		if((i % constants.NO_OF_TABS_AT_A_TIME) != 0):
			webbrowser.open_new_tab("https://pastebin.com/"+list_of_paste_urls[i-1])
			i+=1
		else:
			if input('Do You Want To Continue? [y/n]') != 'y':
				quit()
			else:
				webbrowser.open_new_tab("https://pastebin.com/"+list_of_paste_urls[i-1])
				i+=1

def open_all_pastes():
	"""
	Opens all the urls in the default web browser limited to selected
	no of tabs as decided by constants.NO_OF_TABS_AT_A_TIME
	
    """
	len_list = len(paste_url_users)
	i = 1
	while i <= len_list:
		if((i % constants.NO_OF_TABS_AT_A_TIME) != 0):
			webbrowser.open_new_tab("https://pastebin.com/u/"+paste_url_users[i-1])
			i+=1
		else:
			if input('Do You Want To Continue? [y/n]') != 'y':
				quit()
			else:
				webbrowser.open_new_tab("https://pastebin.com/u/"+paste_url_users[i-1])
				i+=1

if __name__ == '__main__':
	# get previous values to avoid redundant already crawled pastes
	load_keys_to_list()
	load_users_to_list()
	#open_all_pastes()
	get_250_pastes()
	asyncio.run(scrape_urls_for_keyword())
	














