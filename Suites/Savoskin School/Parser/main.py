import requests
from bs4 import BeautifulSoup
import time
import pyautogui as pag
# http://sawshool5.ucoz.com/index/rekomendacii/0-232


# ###########################################     ПАРСЕР ДАННЫХ СО ВСЕХ СТРАНИЦ САЙТА     ###########################################
# with open('links.txt', 'r', encoding='utf-8') as f:
#     links = f.read().splitlines()
#     for link in links:
#         r = requests.get(link)
#         soup = BeautifulSoup(r.text, 'lxml')
#         content_a = soup.find(class_ = 'content-block').find_all('a')
#         content_span = soup.find(class_ = 'content-block').find_all('span')

#         if content_span:
#             filename = link.split('/')[4]
#             my_file = open(f"{filename}.txt", "w")
#             my_file.write(str(link))
#             my_file.write('\n\n\n')
#             print(link)
#             for content_span_tag in content_span:
#                 # print(content_span_tag)
#                 print(content_span_tag.text)
#                 # my_file.write(str(content_span_tag))
#                 # my_file.write('\n')
#                 my_file.write(str(content_span_tag.text.replace('\u0306', '').replace('\u202f', '').replace('\u2757', '')))
#                 my_file.write('\n')
#             my_file.close()
#         elif content_a:
#             filename = link.split('/')[4]
#             my_file = open(f"{filename}.txt", "w")
#             my_file.write(str(link))
#             my_file.write('\n\n\n')
#             print(link)
#             for content_a_tag in content_a:
#                 print(content_a_tag.text)
#                 my_file.write(str(content_a_tag))
#                 my_file.write('\n')
#                 my_file.write(str(content_a_tag.text))
#                 my_file.write('\n')
#             my_file.close()
#         time.sleep(2)

# for link in links:
#     url=link

#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'lxml')
#     # uMenuRoot = soup.find(class_ = 'uMenuRoot').find_all('a')
#     # content_a = soup.find(class_ = 'content-block').find_all('a')
#     content_span = soup.find(class_ = 'content-block').find_all('span')
#     # content_img = soup.find(class_ = 'content-block').find_all('img')

#     # if content_span:
#     filename = link.split('/')[4]
#     my_file = open(f"{filename}.txt", "w")
#     my_file.write(str(link))
#     my_file.write('\n\n\n')
#     print(link)
#     for content_span_tag in content_span:
#         # print(content_span_tag)
#         print(content_span_tag.text)
#         # my_file.write(str(content_span_tag))
#         # my_file.write('\n')
#         my_file.write(str(content_span_tag.text.replace('\u0306', '').replace('\u202f', '').replace('\u2757', '')))
#         my_file.write('\n')
#     my_file.close()


#     elif content_a:
#         filename = link.split('/')[4]
#         my_file = open(f"{filename}.txt", "w")
#         my_file.write(str(link))
#         my_file.write('\n\n\n')
#         print(link)
#         for content_a_tag in content_a:
#             print(content_a_tag.text)
#             my_file.write(str(content_a_tag))
#             my_file.write('\n')
#             my_file.write(str(content_a_tag.text))
#             my_file.write('\n')
#         my_file.close()
#     time.sleep(1)



# ###############################################     ПАРСЕР ЭЛЕМЕНТОВ МЕНЮ     ################################################
# url='http://sawshool5.ucoz.com/'

# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'lxml')
# uMenuRoot = soup.find(class_ = 'uMenuRoot').find_all('a')

# my_file = open('links.txt', 'w')
# for uMenuItem in uMenuRoot:
#     link = uMenuItem.get('href')
#     my_file.write(f'{link}\n')
#     # my_file.write(uMenuItem.text)
#     # my_file.write('\n')
#     # my_file.write(link)
#     # my_file.write('\n')
#     # my_file.write('\n')
# my_file.close()

# ###############################################     HTML ШАБЛОН     ################################################
# with open('namelinks_translit_zip.txt', 'r', encoding='utf-8') as f:
#     namelinks_translit_zip = f.read().splitlines()
# with open('namelinks.txt', 'r') as f:
#     namelinks = f.read().splitlines()
# fin = dict(zip(namelinks_translit_zip, namelinks))

# for k, v in fin.items():
#     my_file = open(f'{k}.html', 'w', encoding='utf-8')
#     my_file.write(f"(% extends 'school/base.html' %)\n\n")
#     my_file.write(f"(% block name_page %)\n")
#     my_file.write(f"\t<div class='name_page_div'>\n")
#     my_file.write(f"\t\t<p class='name_page'>{v}</p>\n")
#     my_file.write(f"\t</div>\n")
#     my_file.write(f"(% endblock %)\n\n")
#     my_file.write(f"(% block content %)\n\n")
#     my_file.write(f"\t(% for item in {k} %)\n")
#     my_file.write(f"\t\t(% if item.photo %)\n")
#     my_file.write(f"\t\t\t<img src='(( item.photo.url ))' alt=''>\n")
#     my_file.write(f"\t\t(% elif item.files %)\n")
#     my_file.write(f"\t\t\t<a href='(( item.files.url ))'>(( item.files ))</a>\n")
#     my_file.write(f"\t\t(% else %)\n")
#     my_file.write(f"\t\t\t<div class='content__left-div'>\n")
#     my_file.write(f"\t\t\t\t<p class='zaglav'>(( item.title ))</p>\n")
#     my_file.write(f"\t\t\t\t<p class='text'>(( item.content|safe ))</p>\n")
#     my_file.write(f"\t\t\t\t<p>(( item.created_at ))</p>\n")
#     my_file.write(f"\t\t\t</div>\n")
#     my_file.write(f"\t\t(% endif %)\n")
#     my_file.write(f"\t(% endfor %)\n\n")
#     my_file.write(f"(% endblock %)\n\n")
#     my_file.close()



# ###############################################     VIEWS.PY     ################################################
# with open('namelinks_translit_zip.txt', 'r', encoding='utf-8') as f:
#     namelinks_translit_zip = f.read().splitlines()

# my_file = open('views.py', 'w', encoding='utf-8')
# for k in namelinks_translit_zip:
#     my_file.write(f'def {k}(request):\n')
#     my_file.write(f'\t{k} = {k.title()}.objects.all()\n')
#     my_file.write(f"\treturn render (request, 'school/other/{k}.html', ('{k}': {k});\n\n")
# my_file.close()



# ###############################################     ADMIN.PY     ################################################
# with open('namelinks_translit_zip.txt', 'r', encoding='utf-8') as f:
#     namelinks_translit_zip = f.read().splitlines()

# my_file = open('admin.py', 'w', encoding='utf-8')
# for k in namelinks_translit_zip:
#     my_file.write(f'class {k.title()}AdminForm(forms.ModelForm):\n')
#     my_file.write(f"\tcontent = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())\n")
#     my_file.write(f'\tclass Meta:\n')
#     my_file.write(f'\t\tmodel = {k.title()}\n')
#     my_file.write(f"\t\tfields = '__all__'\n")
#     my_file.write(f'class {k.title()}Admin(admin.ModelAdmin):\n')
#     my_file.write(f"\tlist_display = 'id', 'title', 'created_at'\n")
#     my_file.write(f"\tlist_display_links = 'id', 'title'\n")
#     my_file.write(f"\tsearch_fields = 'title', 'content'\n")
#     my_file.write(f'\tform = {k.title()}AdminForm\n\n')
# my_file.close()



# with open('namelinks_translit_zip.txt', 'r', encoding='utf-8') as f:
#     namelinks_translit_zip = f.read().splitlines()

# my_file = open('adminregister.py', 'w', encoding='utf-8')
# for k in namelinks_translit_zip:
#     my_file.write(f'admin.site.register({k.title()}, {k.title()}Admin)\n')
# my_file.close()



# ###############################################     MODELS.PY     ################################################
# with open('namelinks_translit_zip.txt', 'r', encoding='utf-8') as f:
#     namelinks_translit_zip = f.read().splitlines()
# with open('namelinks.txt', 'r') as f:
#     namelinks = f.read().splitlines()
# fin = dict(zip(namelinks_translit_zip, namelinks))

# my_file = open('models.py', 'w', encoding='utf-8')
# for k, v in fin.items():
#     my_file.write(f"class {k.title()}(models.Model):\n")
#     my_file.write(f"\ttitle = models.CharField(max_length=150, blank=True, verbose_name='Наименование')\n")
#     my_file.write(f"\tcontent = models.TextField(blank=True, verbose_name='Текст записи')\n")
#     my_file.write(f"\tcreated_at = models.DateField(auto_now_add=True, blank=True, verbose_name='Дата публикации')\n")
#     my_file.write(f"\tphoto = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')\n")
#     my_file.write(f"\tfiles = models.FileField(upload_to='file/%Y/%m/%d/', blank=True, verbose_name='Файл')\n\n")
#     my_file.write(f"\tdef __str__(self):\n")
#     my_file.write(f"\t\treturn self.title\n\n")
#     my_file.write(f"\tclass Meta:\n")
#     my_file.write(f"\t\tverbose_name = 'Запись'\n")
#     my_file.write(f"\t\tverbose_name_plural = '{v}'\n")
#     my_file.write(f"\t\t# ordering = ['-created_at']\n\n")
# my_file.close()



# ###############################################     URLS.PY     ################################################
# with open('namelinks_translit.txt', 'r', encoding='utf-8') as f:
#     namelinks_translit = f.read().splitlines()

# my_file = open('urls.py', 'w', encoding='utf-8')
# for i in namelinks_translit:
#     namelinks_translit_replace = i.replace('"', '').replace(',', '').replace('(', '').replace(')', '').replace("'", "").replace(' ', '-').lower()
#     namelinks_translit_replace_update = namelinks_translit_replace.replace('-', '')
#     my_file.write(f"path('{namelinks_translit_replace}/', views.{namelinks_translit_replace_update}, name='{namelinks_translit_replace}'),\n")
# my_file.close()



# ###############################################     MENU_LINKS     ################################################
# with open('namelinks_translit.txt', 'r', encoding='utf-8') as f:
#     namelinks_translit = f.read().splitlines()
# with open('namelinks.txt', 'r') as f:
#     namelinks = f.read().splitlines()
# fin = dict(zip(namelinks_translit, namelinks))

# my_file = open('menu.txt', 'w', encoding='utf-8')
# for k, v in fin.items():
#     namelinks_translit_replace = k.replace('"', '').replace(',', '').replace('(', '').replace(')', '').replace("'", "").replace(' ', '-').lower()
#     namelinks_translit_replace_update = namelinks_translit_replace.replace('-', '')
#     my_file.write(f'<a class="dropdown__content-link" href="(% url |{namelinks_translit_replace}| %)">{v}</a>\n')
# my_file.close()



# ###############################################     ЗАМЕНА СКОБОК     ################################################
# with open('namelinks_translit_zip.txt', 'r', encoding='utf-8') as f:
#     namelinks_translit_zip = f.read().splitlines()

# for i in namelinks_translit_zip:
#     with open(f'{i}.html', 'r', encoding='utf-8') as f:
#         old = f.read()

#     new = old.replace(')', '}')

#     with open (f'{i}.html', 'w', encoding='utf-8') as f:
#         f.write(new)













# time.sleep(3)
# i = 0
# while True:
#     i += 1
#     if i <= 500:
#         pag.typewrite('n')
#         pag.press('enter')
#         time.sleep(0.1)
#     else:
#         pass