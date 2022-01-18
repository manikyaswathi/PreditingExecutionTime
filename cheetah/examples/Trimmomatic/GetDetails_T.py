import pandas as pd
import re, os, json
import psutil
import platform
from datetime import datetime



df = pd.DataFrame(columns = [])
meta_data = {}
tmp_dir = os.getcwd()
cur_dir = os.path.basename(os.path.normpath(tmp_dir))
meta_data['run_config']=cur_dir



uname = platform.uname()
meta_data['sys_name']=uname.system
meta_data['sys_processor']=uname.processor
cpufreq = psutil.cpu_freq()
meta_data['sys_phy_cores_count']=psutil.cpu_count(logical=False)
meta_data['sys_tot_cores_count']=psutil.cpu_count(logical=True)
tmp = [cpufreq.max, cpufreq.min, cpufreq.current]
meta_data['sys_cpufreq_mhz']=max(tmp)
svmem = psutil.virtual_memory()
swap = psutil.swap_memory()
meta_data['sys_phy_mem_bytes']=svmem.total
meta_data['sys_swap_mem_bytes']=swap.total


fob = {}
with open('codar.cheetah.run-params.json') as f:
    fob = json.load(f)

for exe in fob.keys():
    for setting in fob[exe].keys():
        if setting == "threads":
            print(setting, ":", fob[exe][setting])
            li = fob[exe][setting].split(" ")
            meta_data["run_threads"]=int(li[1])
        elif setting == "IClip":
            # print(setting, ":", fob[exe][setting])
            li = fob[exe][setting].split(":")
            meta_data["run_seedMismatch"]=int(li[2])
            meta_data["run_palindromeClipThreshold"]=int(li[3])
            meta_data["run_simpleClipThreshold"]=int(li[4])
        elif setting == "LEADING_TRAILING":
            print(setting, ":", fob[exe][setting])
            li = fob[exe][setting].split(" ")
            li1 = li[0].split(":")
            meta_data["run_leading"]=int(li1[1])
            li2 = li[1].split(":")
            meta_data["run_trailing"]=int(li2[1])
        elif setting == "SlidingWindow":
            # print(setting, ":", fob[exe][setting])
            li = fob[exe][setting].split(":")
            meta_data["run_sliding_size"]=int(li[1])
            meta_data["run_sliding_quality"]=int(li[2])
        elif setting == "MinLength_MaxInfo":
            #print(setting, ":", fob[exe][setting])
            li = fob[exe][setting].split(" ")
            li1 = li[0].split(":")
            meta_data["run_minlen"]=int(li1[1])
            li2 = li[1].split(":")
            meta_data["run_mi_length"]=int(li2[1])
            meta_data["run_mi_strict"]=float(li2[2])
        else:
            # print("*", setting, ":", fob[exe][setting])
            k_setting = "run_"+setting
            meta_data[k_setting]=fob[exe][setting]
    



total_exe_time = 0
with open('codar.savanna.total.walltime') as f:
    data = f.read()
    total_exe_time = float(data.strip())
    meta_data['total_exe_time_s'] = total_exe_time

    
data = ''
with open('PPROF_data.txt') as f:
    data = f.read()
list_of_tables = data.split('\n\n')

bytes_read = []
bytes_written = []
read_bw = []
write_bw = []
for tab in list_of_tables:
    table = tab.split('\n')
    if table[0].strip() == 'FUNCTION SUMMARY (total):':
        for line in table:
            cells = re.sub(r'\s+', '\t', line.strip())
            cells = cells.split('\t')
            res = cells[:6]+['_'.join(cells[6:])]
            if len(res) == 7 and res[6].strip() == '.TAU_application':
                meta_data['total_wt_tau_time_ms'] = int(res[2])
    if 'USER EVENTS Profile :' in table[0].strip():
        for line in table:
            cells = re.sub(r'\s+', '\t', line.strip())
            cells = cells.split('\t')
            res = cells[:5]+['_'.join(cells[5:])]
            if len(res) == 6:
                last_cell = res[5]
                if 'Bytes_Read' in last_cell:
                    bytes_read.append(float(res[1].strip()))
                if 'Bytes_Written' in last_cell:
                    bytes_written.append(float(res[1].strip()))
                if 'Read_Bandwidth' in last_cell:
                    read_bw.append(float(res[1].strip()))
                if 'Write_Bandwidth' in last_cell:
                    write_bw.append(float(res[1].strip()))
# print("bytes_read", max(bytes_read))
meta_data['max_bytes_read_mb'] = max(bytes_read)
# print("bytes_written", max(bytes_written))
meta_data['max_bytes_written_mb'] = max(bytes_written)
# print("read_bw", max(read_bw))
meta_data['max_read_bw_mbps'] = max(read_bw)
# print("write_bw", max(write_bw))
meta_data['max_write_bw_mbps'] = max(write_bw)
       	 

df = pd.DataFrame([meta_data])
file_name = 'codar.post.details.'+cur_dir+'.csv'
df.to_csv('../'+file_name, header=True, index=False)



