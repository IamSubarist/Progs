import webbrowser
import pyautogui as pg
import time
from gtts import gTTS
import os

# Спокойной ночи❤❤
pg.moveTo(300, 210)
pg.dragTo(440, 210, 0.2)
pg.hotkey('ctrl', 'c')
# webbrowser.open('https://vk.com/im?sel=386465996')
time.sleep(20)
pg.click(758, 715)
pg.hotkey('ctrl', 'v')
time.sleep(1)
pg.typewrite(['enter'])
time.sleep(1)
pg.hotkey('ctrl', 'w')

pg.moveTo(319, 767)
time.sleep(0.2)
pg.moveTo(319, 680, 0.2)
pg.leftClick()
time.sleep(0.2)
pg.click(768, 307)
time.sleep(0.2)
pg.scroll(-1000)
time.sleep(1)

# Спокойной ночи❤❤😘 
pg.moveTo(300, 230)
pg.dragTo(460, 230, 0.2)
pg.hotkey('ctrl', 'c')
pg.hotkey('ctrl', 'w')
webbrowser.open('https://vk.com/im?sel=309059107')

time.sleep(20)
pg.click(758, 715)
pg.hotkey('ctrl', 'v')
time.sleep(1)
pg.typewrite(['enter'])
time.sleep(1)
pg.hotkey('ctrl', 'w')

# pg.moveTo(319, 767)
# time.sleep(0.2)
# pg.moveTo(319, 680, 0.2)
# pg.leftClick()
# time.sleep(0.2)
# pg.click(768, 307)
# time.sleep(0.2)
# pg.scroll(-1000)
# time.sleep(1)

# """
# Спокойной ночи❤
# Добрых снов❤
# Люблю❤
# """
# pg.moveTo(286, 270)
# pg.dragTo(340, 305, 0.2)
# pg.hotkey('ctrl', 'c')
# webbrowser.open('https://vk.com/im?sel=293896528')
# time.sleep(20)
# pg.click(758, 715)
# pg.hotkey('ctrl', 'v')
# time.sleep(1)
# pg.typewrite(['enter'])
# time.sleep(1)
# pg.hotkey('ctrl', 'w')

text = 'Спокойной ночи, Роман Александрович! Увидимся утром.'
speech = gTTS(text=text, lang='ru', slow=False)
speech.save('goodnight.mp3')
os.system('goodnight.mp3')

time.sleep(5)
pg.hotkey('winleft')
time.sleep(0.5)
pg.click(452, 708)
time.sleep(0.5)
pg.click(508, 708)