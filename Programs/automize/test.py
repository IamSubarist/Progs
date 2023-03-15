import pyautogui as pg
# from gtts import gTTS
# import os
# from turtle import *
# import time
while True:
    pg.typewrite(['enter'])
# path_a = 'C:/Users/User/Desktop/arbeitet'
# path_b = 'C:/Users/User/Desktop/вырезать фон 9 NOV'

# # a = []
# # b = []

# for root, dirs, files in os.walk(path_a):
#     for filename_a in files:
#         a = filename_a
#         f = open('a.txt', 'a+')
#         f.write(filename_a)
#         f.write('\n')
#         f.close()

# for root, dirs, files in os.walk(path_b):  
#     for filename_b in files:
#         b = filename_b
#         f = open('b.txt', 'a+')
#         f.write(filename_b)
#         f.write('\n')
#         f.close()

# # path_c = 'C:/Users/User/Desktop/Promezh'

# file1 = open("a.txt",'r')        
# file2 = open("b.txt",'r')
# NewFile = open("difference.txt",'w')

# for line1 in file1:
#     if line1 not in file2:
#         NewFile.write(line1)

# file1.close()
# file2.close()
# NewFile.close()



# # file1 = open("a.txt",'r')        
# # file2 = open("b.txt",'r')
# NewFile = open("difference.txt",'r')

# for line1 in NewFile:
#     line = line1.replace('\n', '')
#     print(line)

# # file1.close()
# # file2.close()
# NewFile.close()



# res = [x for x in a + b if x not in a or x not in b]

# print(res)
# f = open('not_equal.txt', 'a+')
# f.write(res)
# f.write('\n')
# f.close()













# while 1 == 1:
#     print(pg.position())



# Проверка.
# time.sleep(5)
# for i in range(1000):
#     pg.hotkey('ctrl', 'v')
#     time.sleep(0.5)
#     pg.typewrite(['enter'])
#     print(i + 1, 'message send')



# text = 'Егор клоун. Официально подтверждаю.'
# speech = gTTS(text=text, lang='ru', slow=False)
# speech.save('good.mp3')
# os.system('good.mp3')

# def petal():
#     begin_fill(),
#     circle(50, 90)
#     left(90)
#     circle(50, 90)
#     end_fill()
#     left(18)

# def flower():
#     for i in range(5):
#         petal()

# def love():
#     circle(100, 90)
#     circle(50, 90)
#     circle(50, 90)
#     left(180)
#     circle(50, 90)
#     circle(50, 90)
#     circle(100, 90)

# width(2)
# Screen().title('Для любимой!')
# fillcolor('violet')
# Screen().bgcolor('black')
# pencolor('white')
# flower()
# penup()
# goto(80, 20)
# pendown()
# flower()
# penup()
# goto(40, 100)
# pendown()
# flower()
# time.sleep(1)
# Screen().clear()
# width(5)
# fillcolor('red')
# Screen().bgcolor('black')
# pencolor('red')
# love()
# time.sleep(1)
# Screen().bye()
# done()