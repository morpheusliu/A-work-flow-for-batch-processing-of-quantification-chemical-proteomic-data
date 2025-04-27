import shutil
import os
import subprocess
import glob
import time
file_time=open('time','wt')
file_localt=open('localtime','wt')
file_cpu=open('cpu','wt')
file_pro_con=open('control_project.txt','rt')
while True:
	data_pro_con=file_pro_con.readline().replace('\n','')
	if not data_pro_con:
		break
	if data_pro_con.startswith('path_data='):
		pd=data_pro_con[data_pro_con.find('=')+1:]
	if data_pro_con.startswith('path_thermorawreader_out='):
		pto=data_pro_con[data_pro_con.find('=')+1:]
	if data_pro_con.startswith('path_bin='):
		pb=data_pro_con[data_pro_con.find('=')+1:]
	if data_pro_con.startswith('path_calculationsystem='):
		pcs=data_pro_con[data_pro_con.find('=')+1:]
	if data_pro_con.startswith('mms='):
		mms=data_pro_con[data_pro_con.find('=')+1:]
	if data_pro_con.startswith('maxr='):
		maxr=data_pro_con[data_pro_con.find('=')+1:]
	if data_pro_con.startswith('minr='):
		minr=data_pro_con[data_pro_con.find('=')+1:]
	if data_pro_con.startswith('minin='):
		minin=data_pro_con[data_pro_con.find('=')+1:]
	if data_pro_con.startswith('modi='):
		modi=data_pro_con[data_pro_con.find('=')+1:]
	if data_pro_con.startswith('mode='):
		mode=data_pro_con[data_pro_con.find('=')+1:]
file_pro_con.close()

if os.path.exists('pquant_post_processing\\data_protein'):						
	shutil.rmtree('pquant_post_processing\\data_protein')
	os.makedirs('pquant_post_processing\\data_protein')
else:
	os.makedirs('pquant_post_processing\\data_protein')

if os.path.exists('pquant_post_processing\\data'):							
	shutil.rmtree('pquant_post_processing\\data')
	os.makedirs('pquant_post_processing\\data')
else:
	os.makedirs('pquant_post_processing\\data')

if os.path.exists('data_split'):							
	shutil.rmtree('data_split')
	os.makedirs('data_split')
else:
	os.makedirs('data_split')

print('----------------MSReader is working----------------')
start=time.time()
arry_file=glob.glob(pd+'\\*')
os.chdir('ThermoRawRead_ctarn_split_cv')
for file in arry_file:
	file_name=file[file.rfind('\\')+1:].replace('.raw','')
	print("ThermoRawRead.exe -D "+file+" -O "+"data\\split\\"+file_name+" -c")
	subprocess.call("ThermoRawRead.exe -D "+file+" -O "+pto+'\\'+file_name+" -c")
end=time.time()
print('MSReader\t'+str(end-start),file=file_time)
print('MSReader\t'+str(start)+'\t'+str(end),file=file_localt)


print('----------------pParse is working----------------')
start=time.time()
arry_all_data_dir=[]
arry_dir=glob.glob(pto+'\\*')
for dir in arry_dir:
	arry_all_raw=[]
	arry_secdir=[]
	arry_secdir=glob.glob(dir+'\\*')
	arry_all_data_dir.append(dir)
	for secd in arry_secdir:
		pure_secd=secd[secd.rfind('\\')+1:]
		arry_file=[]
		arry_file=glob.glob(secd+'\\*')
		for file in arry_file:
			pure_file=file[file.rfind('\\')+1:]
			if '45' in pure_secd and not '\\45_' in file:
				os.rename(file,file[:file.rfind('\\')+1]+'45_'+pure_file)
			elif '65' in pure_secd and not '\\65_' in file:
				os.rename(file,file[:file.rfind('\\')+1]+'65_'+pure_file)
	for secd in arry_secdir:
		arry_file=[]
		arry_file=glob.glob(secd+'\\*')
		for file in arry_file:
			if file.endswith('.ms1') or file.endswith('.ms2'):
				file_data=open(file,'rt')
				arry_data=file_data.readlines()
				file_data.close()
				file_result=open(file,'wt')
				for data in arry_data:
					if '\tRetentionTime\t' in data:
						data=data.replace('\tRetentionTime\t','\tRetTime\t')
					print(data.replace('\n',''),file=file_result)
				file_result.close()
		for file in arry_file:
			if file.endswith('raw'):
				arry_all_raw.append(file)
	for secd in arry_secdir:
		arry_ms1=glob.glob(secd+'\\*.ms1')
		print(arry_ms1)
		arry_ms2=glob.glob(secd+'\\*.ms2')
		print(arry_ms2)
		arry_sn=[]
		file_ms1=open(arry_ms1[0],'rt')
		arry_data_ms1=file_ms1.readlines()
		file_ms1.close()
		for ds1 in arry_data_ms1:
			if ds1.startswith('S\t'):
				arry_ds1=ds1.split('\t')
				arry_sn.append(int(arry_ds1[1]))
		file_ms2=open(arry_ms2[0],'rt')
		arry_data_ms2=file_ms2.readlines()
		file_ms2.close()
		for ds2 in arry_data_ms2:
			if ds2.startswith('S\t'):
				arry_ds2=ds2.split('\t')
				arry_sn.append(int(arry_ds2[1]))
		arry_sn.sort()
		file_ms1=open(arry_ms1[0],'wt')
		for dms1 in arry_data_ms1:
			dms1=dms1.replace('\n','')
			if not dms1.startswith('S\t'):
				print(dms1,file=file_ms1)
			else:
				arry_dms1=dms1.split('\t')
				arry_dms1[1]=str(arry_sn.index(int(arry_dms1[1]))+1)
				arry_dms1[2]=str(arry_sn.index(int(arry_dms1[2]))+1)
				print('S\t'+arry_dms1[1]+'\t'+arry_dms1[2],file=file_ms1)
		file_ms1.close()
		file_ms2=open(arry_ms2[0],'wt')
		for dms2 in arry_data_ms2:
			dms2=dms2.replace('\n','')
			if dms2.startswith('S\t'):
				arry_dms2=dms2.split('\t')
				arry_dms2[1]=str(arry_sn.index(int(arry_dms2[1]))+1)
				arry_dms2[2]=str(arry_sn.index(int(arry_dms2[2]))+1)
				print('S\t'+arry_dms2[1]+'\t'+arry_dms2[2],file=file_ms2)
			elif dms2.startswith('I\tPrecursorScan\t'):
				arry_dms2=dms2.split('\t')
				arry_dms2[2]=str(arry_sn.index(int(arry_dms2[2]))+1)
				print(('\t').join(arry_dms2),file=file_ms2)
			else:
				print(dms2,file=file_ms2)
		file_ms2.close()
	if not os.path.exists(dir+'\\search_results'):
		os.mkdir(dir+'\\search_results')
	os.chdir(pcs)
	file_pcfg=open('cfg\\pParse.cfg','rt')
	file_rpcfg=open(dir+'\\pParse.cfg','wt')
	type=0
	while True:
		data_pcfg=file_pcfg.readline().replace('\n','')
		if data_pcfg.startswith('Intensity='):
			type=1
		if not data_pcfg and type==1:
			break
		if data_pcfg.startswith('datapath1='):
			print(data_pcfg+arry_all_raw[0],file=file_rpcfg)
		elif data_pcfg.startswith('datapath2='):
			print(data_pcfg+arry_all_raw[1],file=file_rpcfg)
		else:
			print(data_pcfg,file=file_rpcfg)
	file_pcfg.close()
	file_rpcfg.close()
	os.chdir(pb)
	print('pParse.exe '+dir+'\\pParse.cfg')
	subprocess.call('pParse.exe '+dir+'\\pParse.cfg')
end=time.time()
print('pParse\t'+str(end-start),file=file_time)
print('pParse\t'+str(start)+'\t'+str(end),file=file_localt)

for dir in arry_all_data_dir:
	os.chdir(pcs)
	file_pfc=open('cfg\\pFind.cfg','rt')
	file_result=open(dir+'\\pFind.cfg','wt')
	type=0
	while True:
		data_pfc=file_pfc.readline().replace('\n','')
		if data_pfc.startswith('log='):
			type=1
		if not data_pfc and type==1:
			break
		if data_pfc.startswith('msmspath1='):
			print(data_pfc+glob.glob(dir+'\\CV-45\\*.pf2')[0],file=file_result)
		elif data_pfc.startswith('msmspath2='):
			print(data_pfc+glob.glob(dir+'\\CV-65\\*.pf2')[0],file=file_result)
		elif data_pfc.startswith('outputpath='):
			print(data_pfc+dir+'\\search_results\\',file=file_result)
		elif data_pfc.startswith('outputname='):
			print(data_pfc+'search_result',file=file_result)
		else:
			if data_pfc.startswith('fastapath='):
				database=data_pfc[data_pfc.rfind('=')+1:]
			print(data_pfc,file=file_result)
	file_pfc.close()
	file_result.close()
	file_pgq=open('cfg\\pGlycoQuant_cfg.txt','rt')
	file_result=open(dir+'\\pGlycoQuant_cfg.txt','wt')
	type=0
	while True:
		data_pgq=file_pgq.readline().replace('\n','')
		if data_pgq.startswith('FLAG_CREATE_NEW_FOLDER='):
			type=1
		if not data_pgq and type==1:
			break
		if data_pgq.startswith('PATH_MS1='):
			print(data_pgq+glob.glob(dir+'\\CV-45\\*.ms1')[0]+'|'+glob.glob(dir+'\\CV-65\\*.ms1')[0],file=file_result)
		elif data_pgq.startswith('PATH_MS2='):
			print(data_pgq+glob.glob(dir+'\\CV-45\\*.ms2')[0]+'|'+glob.glob(dir+'\\CV-65\\*.ms2')[0],file=file_result)
		elif data_pgq.startswith('PATH_IDENTIFICATION_RESULT='):
			print(data_pgq+dir+'\\search_results\\pFind-Filtered.spectra',file=file_result)
		elif data_pgq.startswith('PATH_EXPORT='):
			print(data_pgq+dir+'\\search_results\\',file=file_result)
		else:
			print(data_pgq,file=file_result)
	file_pgq.close()
	file_result.close()
	os.chdir(pb)
	print('----------------pFind is working----------------')
	start=time.time()
	subprocess.call('Searcher.exe '+dir+'\\pFind.cfg')
	end=time.time()
	print('pFind\t'+str(end-start),file=file_time)
	print('pFind\t'+str(start)+'\t'+str(end),file=file_localt)
	print('----------------New pQuant is working----------------')
	os.chdir(pcs)
	os.chdir('pGlycoQuant')
	start=time.time()
	subprocess.call('pGlycoQuant.exe '+dir+'\\pGlycoQuant_cfg.txt')
	end=time.time()
	print('New pQuant\t'+str(end-start),file=file_time)
	print('New pQuant\t'+str(start)+'\t'+str(end),file=file_localt)

for dir in arry_all_data_dir:
	dir_name=dir[dir.rfind('\\')+1:]
	arry_all_file=glob.glob(dir+'\\search_results\\*')
	for file in arry_all_file:
		if file.endswith('pGlycoQuant.spectra.list'):
			shutil.copy(file,pcs+'\\pquant_post_processing\\data\\'+dir_name)
		if file.endswith('pFind.protein'):
			shutil.copy(file,pcs+'\\pquant_post_processing\\data_protein\\'+dir_name+'_p')

print('----------------SLCP is working----------------')
arry_all_data=glob.glob(pcs+'\\pquant_post_processing\\data\\*')
os.chdir(pcs+'\\pquant_post_processing')
file_database=open(database,'rt')
n=0;
while True:
	data_database=file_database.readline()
	if not data_database:
		break
	if data_database.startswith('>') and not data_database.startswith('>CON_'):
		n+=1
		if n%1000==0:
			print(n)
		arry_data_database=data_database.split('|')
		file_description=open('description/'+arry_data_database[1],'wt')
		file_description.write(arry_data_database[2])
file_description.close()
file_database.close()
file_control=open('control.txt','wt')
for data in arry_all_data:
	print('filename='+data[data.rfind('\\')+1:]+' mms='+mms+' maxr='+maxr+' minr='+minr+' minin='+minin+' modi='+modi+' mode='+mode,file=file_control)
file_control.close()
start=time.time()
subprocess.call('python main_post_new_pquant.py')
end=time.time()
print('SLCP\t'+str(end-start),file=file_time)
print('SLCP\t'+str(start)+'\t'+str(end),file=file_localt)

file_time.close()
file_localt.close()
