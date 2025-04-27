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

if os.path.exists('pquant_post_processing\\data'):								
	shutil.rmtree('pquant_post_processing\\data')
os.makedirs('pquant_post_processing\\data')

if not os.path.exists(pto):								
	os.makedirs(pto)

print('----------------MSReader is working----------------')
start=time.time()
arry_file=glob.glob(pd+'\\*.raw')												
print(arry_file)
os.chdir(pb)
for file in arry_file:
	file_name=file[file.rfind('\\')+1:].replace('.raw','')
	if os.path.exists(pto+'\\'+file_name):
		shtil.rmtree(pro+'\\'+file_name)
	os.mkdir(pto+'\\'+file_name)
	subprocess.call("xtract_raw.exe -ms -a -i 1 -m 5 -o "+pto+'\\'+file_name+" "+file)
end=time.time()
print('MSReader\t'+str(end-start),file=file_time)
print('MSReader\t'+str(start)+'\t'+str(end),file=file_localt)

arry_final_files=glob.glob(pd+'\\*')
for file in arry_final_files:
	file_name=file[file.rfind('\\')+1:]
	final_name=file[file.rfind('\\')+1:file.find('.')]
	shutil.copy(file,pto+'\\'+final_name+'\\'+file_name)

print('----------------pParse is working----------------')
start=time.time()
arry_all_data_dir=[]
arry_dir=glob.glob(pto+'\\*')
for dir in arry_dir:
	final_name=dir[dir.rfind('\\')+1:]
	arry_all_data_dir.append(dir)
	if not os.path.exists(dir+'\\search_results'):
		os.mkdir(dir+'\\search_results')
	if not os.path.exists(dir+'\\param'):
		os.mkdir(dir+'\\param')
	os.chdir(pcs)
	file_pcfg=open('cfg\\pParse.cfg_qe','rt')
	file_rpcfg=open(dir+'\\param\\pParse.cfg','wt')
	type=0
	while True:
		data_pcfg=file_pcfg.readline().replace('\n','')
		if data_pcfg.startswith('Intensity='):
			type=1
		if not data_pcfg and type==1:
			break
		if data_pcfg.startswith('datapath1='):
			print(data_pcfg+dir+'\\'+final_name+'.raw',file=file_rpcfg)
		else:
			print(data_pcfg,file=file_rpcfg)
	file_pcfg.close()
	file_rpcfg.close()
	os.chdir(pb)
	subprocess.call('pParse.exe '+dir+'\\param\\pParse.cfg')
end=time.time()
print('pParse\t'+str(end-start),file=file_time)
print('pParse\t'+str(start)+'\t'+str(end),file=file_localt)

for dir in arry_all_data_dir:
	os.chdir(pcs)
	file_pfc=open('cfg\\pFind.cfg_qe','rt')
	file_result=open(dir+'\\param\\pFind.cfg','wt')
	type=0
	while True:
		data_pfc=file_pfc.readline().replace('\n','')
		if data_pfc.startswith('log='):
			type=1
		if not data_pfc and type==1:
			break
		if data_pfc.startswith('msmspath1='):
			print(data_pfc+glob.glob(dir+'\\*.pf2')[0],file=file_result)
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
	file_result=open(dir+'\\param\\pGlycoQuant_cfg.txt','wt')
	type=0
	while True:
		data_pgq=file_pgq.readline().replace('\n','')
		if data_pgq.startswith('FLAG_CREATE_NEW_FOLDER='):
			type=1
		if not data_pgq and type==1:
			break
		if data_pgq.startswith('PATH_MS1='):
			print(data_pgq+glob.glob(dir+'\\*.ms1')[0],file=file_result)
		elif data_pgq.startswith('PATH_MS2='):
			print(data_pgq+glob.glob(dir+'\\*.ms2')[0],file=file_result)
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
	subprocess.call('Searcher.exe '+dir+'\\param\\pFind.cfg')
	end=time.time()
	print('pFind\t'+str(end-start),file=file_time)
	print('pFind\t'+str(start)+'\t'+str(end),file=file_localt)
	print('----------------New pQuant is working----------------')
	os.chdir(pcs)
	os.chdir('pGlycoQuant')
	start=time.time()
	subprocess.call('pGlycoQuant.exe '+dir+'\\param\\pGlycoQuant_cfg.txt')
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
