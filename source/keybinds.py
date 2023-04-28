import json

possible_keybinds = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'ATTACK', 'INTERACT', 'USE_ITEM']

def getKeybinds():
	keybindsFile = open('settings/keybinds.json')
	keybindsData = json.load(keybindsFile)
	keybindsFile.close()
	return keybindsData

keybinds = getKeybinds()

def saveKeybinds():
	keybindsFile = open('settings/keybinds.json', 'w')
	json.dump(keybinds, keybindsFile)
	keybindsFile.close()