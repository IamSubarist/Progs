import os

path = 'C:/Users/User/Desktop/PhotoShop'

i = 0
for filename in os.listdir(path):
  os.rename(path + '/' + filename, filename.replace('.png', '.jpg'))
  i += 1