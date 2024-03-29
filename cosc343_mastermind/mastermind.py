__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

import os,sys
import numpy as np
import importlib
import time
from settings import game_settings
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)
class bcolors:
   RED = '\033[1;30;41m'
   GREEN = '\033[1;30;42m'
   YELLOW = '\033[1;30;43m'
   BLUE = '\033[1;30;44m'
   PURPLE = '\033[1;30;45m'
   CYAN = '\033[1;30;46m'
   ENDC = '\033[0m'

def print_colour_char(c):
   if c == 'B':
      sys.stdout.write(f"{bcolors.BLUE}B{bcolors.ENDC}")
   elif c == 'R':
      sys.stdout.write(f"{bcolors.RED}R{bcolors.ENDC}")
   elif c == 'G':
      sys.stdout.write(f"{bcolors.GREEN}G{bcolors.ENDC}")
   elif c == 'Y':
      sys.stdout.write(f"{bcolors.YELLOW}Y{bcolors.ENDC}")
   elif c == 'C':
      sys.stdout.write(f"{bcolors.CYAN}C{bcolors.ENDC}")
   elif c == 'P':
      sys.stdout.write(f"{bcolors.PURPLE}P{bcolors.ENDC}")
   else:
       sys.stdout.write("%c" % c)
   sys.stdout.flush()

def time_to_str(time_in_seconds):
   timeStr = ''
   if time_in_seconds > 3600:
      hours = int(np.floor(time_in_seconds / 3600))
      timeStr += "%d h, " % hours
      time_in_seconds %= 3600

   if time_in_seconds > 60:
      minutes = int(np.floor(time_in_seconds / 60))
      timeStr += "%d min, " % minutes
      time_in_seconds %= 60

   if time_in_seconds < 1:
      timeStr += "%.1f s" % time_in_seconds
   else:
      timeStr += "%d s" % time_in_seconds

   return timeStr

def evaluate_guess(guess,target):
   """ Evaluates a guess against a target

         :param guess: a list or numpy array of valid colour characters that constitutes a guess

                target: a list or numpy array of valid colour characters that constitutes target solution


         :return: a tuple of 2 integers:

                  - the number of correct colours in place in guess against the target

                  - the number of correct colours out of place in guess against the target

         """


   guess = np.reshape(guess, (-1))
   target = np.reshape(target, (-1))

   I = np.where(guess==target)[0]
   in_place = len(I)
   I = np.where(guess!=target)[0]
   state = np.zeros(np.shape(target))

   in_colour = 0
   for i in I:
      a = target[i]
      for j in I:
         if state[j] != 0:
            continue

         b = guess[j]

         if a==b:
            in_colour += 1
            state[j] = -1
            break

   return in_place, in_colour

# Class player is a wrapper for a player agent
class Player:
   def __init__(self, playerFile,code_length,colours,num_guesses):
      self.playerFile = playerFile

      if not os.path.exists(playerFile):
         raise RuntimeError("Error! Agent file '%s' not found" % self.playerFile)

      if len(playerFile) > 3 and playerFile[-3:].lower() == '.py':
         playerModule = playerFile[:-3]
      else:
         raise RuntimeError("Error! Agent file %s needs a '.py' extension" % self.playerFile)


      try:
         self.exec = importlib.import_module(playerModule)
      except Exception as e:
         raise RuntimeError(str(e))

      try:
         self.agent = self.exec.MastermindAgent(code_length=code_length, colours=colours,num_guesses=num_guesses)
      except Exception as e:
         raise RuntimeError(str(e))


class MastermindGame:

   def __init__(self,code_length=5,num_colours=3,verbose=False,tournament=False):

      self.colours = ['B','R','G','Y','P','C']
      self.code_length = code_length
      self.verbose = verbose
      if tournament:
         self.throwError = self.errorAndReturn
      else:
         self.throwError = self.errorAndExit

      self.colours = self.colours[:num_colours]

      if self.verbose:
         print("Mastermind")

         print("  Code length: %s" % self.code_length)
         print("      Colours: %s" % self.colours)

   def errorAndExit(self,errorStr):
      raise RuntimeError(errorStr)

   def errorAndReturn(self,errorStr):
      self.errorStr = errorStr
      return None



   def play(self,player,target,num_guesses):

      score = 0
      guess = 0
      actions = np.zeros(shape=(self.code_length)).astype('uint8')
      in_place = 0
      in_colour = 0
      while guess<num_guesses+1:

         percepts = (guess, actions, in_place, in_colour)

         try:
            actions = player.agent.AgentFunction(percepts)
         except Exception as e:
            self.throwError(str(e))

         try:
            if not isinstance(actions,list) and not isinstance(actions,np.ndarray):
               if actions == None:
                  score = num_guesses
                  break
               else:
                  self.throwError("Error! AgentFunction from '%s.py' returned a %s (expecting a list or a numpy array)" % (player.playerFile,type(actions)))

         except Exception as e:
            self.throwError(str(e))

         if len(actions) != self.code_length:
            self.throwError(
                  "Error! AgentFunction from '%s.py' did return a list with %d items (expecting %d items)." % (
                     player.playerFile, len(actions), self.code_length))

            for j, a in enumerate(actions):
               if a not in self.colours:
                  self.throwError(
                     "Error! AgentFunction from '%s.py' returned a list \n%s\n, which contains illegal character '%c' (legal characters are %s)."
                     % (player.playerFile, actions, a, self.colours))

         in_place, in_colour = evaluate_guess(actions,target)


         score += 1
         guess += 1

         if self.verbose:

            sys.stdout.write("Guess %2d:\r\n" % (guess))

            sys.stdout.write(u'\u2713' + "%d " % in_place)

            #sys.stdout.write("\n\r")
            #sys.stdout.write("   ");

            for c in actions:
               print_colour_char(c)

            sys.stdout.write(" ?%d\n\r" % in_colour)
            sys.stdout.flush()

            sys.stdout.write("   ")

         if in_place == np.prod(np.shape(target)):
            if self.verbose:
               if score == 1:
                  print("Solved in 1 guess!")
               else:
                  print("Solved in %d guesses!" % score)

            return score

         if guess >= num_guesses:
            break

      if self.verbose:
         print("The solution was: ")
         sys.stdout.write("   ")
         for c in target:
            print_colour_char(c)
         sys.stdout.write("\r\n")
      return score*2


   def run(self,agentFile='agent_human.py',num_guesses=6, num_games=1000,seed=None):

      if self.verbose:
         print("Game play:")
         print("  Num guesses:      %d" % num_guesses)
         print("  Num rounds:       %d" % num_games)

      if seed is None:
         seed = int(time.time())

      rnd = np.random.RandomState(seed)

      try:
         player = Player(playerFile=agentFile,code_length=self.code_length,colours=list(self.colours),num_guesses=num_guesses)
      except Exception as e:
         self.throwError(str(e))

      all_boards = (num_games, self.code_length)

      self.colours = np.array(self.colours)

      I = rnd.randint(0,len(self.colours),size=(all_boards))

      score = 0
      game_count = 0
      tot_time = 0
      for i in I:
         start = time.time()
         score += self.play(player, target=self.colours[i], num_guesses=num_guesses)
         end = time.time()
         game_count += 1
         tot_time += end - start

         if game_count < num_games:
            avg_time = tot_time / game_count
            remaining_time = time_to_str(avg_time * (num_games-game_count))
            expected_total_time = time_to_str(avg_time * num_games)
         else:
            remaining_time = "N/A"
            expected_total_time = time_to_str(tot_time)

         logger.debug("Round {}/{} | Avg score: {:.2f} | Avg time/game: {} | Time remaining: {} | Total expected time: {}"
               .format(game_count, len(I), score/game_count, time_to_str(avg_time), remaining_time, expected_total_time))
      print(("Round {}/{} | Avg score: {:.2f} | Avg time/game: {} Total expected time: {}"
               .format(game_count, len(I), score/game_count, time_to_str(avg_time), tot_time)))









if __name__ == "__main__":

   game = MastermindGame(code_length=game_settings['codeLength'],
                         num_colours=game_settings['numberOfColours'],
                         verbose=game_settings['verbose'])

   game.run(agentFile=game_settings['agentFile'],
         num_guesses=game_settings['maxNumberOfGuesses'],
         num_games=game_settings['totalNumberOfGames'],
         seed=game_settings['seed'])



