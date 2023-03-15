with open('links.txt', 'r', encoding='utf-8') as f:
    links = f.read().splitlines()
for link in links:
	filename = link.split('/')[4]
	if filename == 'organizacija_pitanija_v_obrazovatelnoj_organizacii':
		pass
	elif filename == 'gorjachee_pitanie':
		pass
	elif filename == 'rezhim_pitanija_obuchajushhikhsja_grafik_1_4_klassov':
		pass
	elif filename == 'rezhim_pitanija_obuchajushhikhsja_grafik_poluchajushhikh_lgotnoe_pitanie':
		pass
	elif filename == 'centr_quot_tochka_rosta_quot':
		pass
	elif filename == 'dopolnitelnaja_informacija':
		pass
	elif filename == 'obratnaja_svjaz_kontakty_socialnye_seti':
		pass
	elif filename == 'galereja':
		pass
	elif filename == 'shkolnoe_samoupravlenie':
		pass
	elif filename == 'antiterroristicheskaja_bezopasnost':
		pass
	elif filename == 'upravlencheskie_mekhanizmy_ocenki_kachestva_obrazovanija':
		pass
	elif filename == 'sistema_razvitija_talanta':
		pass
	elif filename == 'sistema_proforientacii':
		pass
	elif filename == 'sozdanie_specialnykh_uslovij_dlja_obuchenija_detej_s_ovz_i_invalidnostju':
		pass
	elif filename == 'dokumenty_shkoly':
		pass
	else:
		file =f'C:\\Users\\user\\Desktop\\Actual\\Parser\\{filename}.txt'

		uniqlines = set(open(file,'r').readlines())
		gotovo = open(file,'w').writelines(set(uniqlines))

# for link in links:
#         link_split = link.split('/')[4]
#         link_replace = link_split.replace('_', '-')
#         print(link_replace)