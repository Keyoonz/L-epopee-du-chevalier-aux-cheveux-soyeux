import json

def load_words() -> None:
	global words
	with open('settings/words.json', encoding='utf-8') as words_file:
		words = json.load(words_file)

def load_dialogues():
	global dialogues
	with open('settings/dialogues.json', encoding='utf-8') as dialogues_file:
		dialogues = json.load(dialogues_file)

def save_language():
	language_file = open('settings/language.json', 'w')
	language_settings = {"language": current_language}
	json.dump(language_settings, language_file)
	language_file.close()

def get_language():
	language_file = open('settings/language.json', 'r')
	language_settings = json.load(language_file)
	return language_settings['language']

current_language = get_language()