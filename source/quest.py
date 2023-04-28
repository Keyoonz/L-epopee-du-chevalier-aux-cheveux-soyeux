import pygame
from data import quests
from item import Item
import words

class Quest:
    def __init__(self, name_id, subquests, reward, inventory) -> None:
        self.name_id = name_id
        self.dialogue = None
        self.subquests = subquests
        self.current_subquest = 0
        self.number_of_subquests = len(subquests)
        self.reward = reward
        self.completed = False
        self.inventory = inventory

        #temp
        self.last_time = pygame.time.get_ticks()

    def update(self):
        if not self.completed:
            self.dialogue = words.dialogues[words.current_language][self.name_id]["name"]
            self.subquests[self.current_subquest].dialogue = words.dialogues[words.current_language][self.name_id][str(self.current_subquest)]
        #Main Quest
        if self.completed and self.reward not in self.inventory.items:
            if self.reward != None:
                self.inventory.items.append(self.reward)
            quests.remove(self)
        
        #Subquests
        if self.current_subquest < self.number_of_subquests and self.subquests[self.current_subquest].completed:
            if self.subquests[self.current_subquest].completed and self.subquests[self.current_subquest].reward not in self.inventory.items:
                if self.subquests[self.current_subquest].reward != None:
                    self.inventory.items.append(self.subquests[self.current_subquest].reward)
            if self.subquests[self.current_subquest].completed and self.subquests[self.current_subquest].new_quest != None:
                quests.append(self.subquests[self.current_subquest].new_quest)
            if self.current_subquest == self.number_of_subquests-1:
                self.completed = True
                self.current_subquest += 1
            else:
                self.current_subquest += 1
        
        if not self.completed:
            if self.subquests[self.current_subquest].current_objective_amount == self.subquests[self.current_subquest].objective_amount:
                self.subquests[self.current_subquest].completed = True

    def check_quest(self, objective, objective_type):
        if not self.completed:
            if self.subquests[self.current_subquest].objective_type != objective_type:
                return
            if objective == self.subquests[self.current_subquest].objective:
                self.subquests[self.current_subquest].current_objective_amount += 1 
        
class Subquest:
    def __init__(self, objective_type, objective, objective_amount, reward, new_quest=None, end_game=False):
        self.dialogue = ""
        self.objective_type = objective_type
        self.objective = objective
        self.objective_amount = objective_amount
        self.current_objective_amount = 0
        self.reward = reward
        self.completed = False
        self.kills = []
        self.new_quest = new_quest
        self.endgame = end_game