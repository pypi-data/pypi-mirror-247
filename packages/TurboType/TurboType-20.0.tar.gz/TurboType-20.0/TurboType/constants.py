from pathlib import Path
from os import path

FPS = 60 # Frames Per Second (FPS)
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
WORDS = [] # WORDS holds all the words available for the game
WORDS_ON_SCREEN = [] # WORDS_ON_SCREEN contains words currently displayed on the game screen.
DIFFICULTY = 3 # The initial difficulty level of the game. This value is used to adjust the game's difficulty based on the player's performance.
DELAY = FPS * DIFFICULTY # the delay (in frames) between generating new words during gameplay. It's calculated based on the product of FPS and DIFFICULTY.
WORD_MOVE_TIME = FPS * 1 # The time (in frames) for a word to move across the screen. This value is set to represent 1 second's duration in terms of frames.
WORDS_POSITION = [-1*x for x in range(0,round(WORD_MOVE_TIME/6))] # WORDS_POSITION is a list of integers that represent the y-axis positions of the words displayed on the screen. The list is used to make sure that words are not displayed on the same line.
user_input = ""
current_score = 0
BG_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
life_count = 3
ANTI_ALIASING = True
FONT_FILE = Path(path.dirname(__file__)) / 'data' / 'font.ttf'
WORDS_FILE = Path(path.dirname(__file__)) / 'data' / 'words.txt'
