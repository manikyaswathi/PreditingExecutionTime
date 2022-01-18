from datetime import datetime, timedelta
import getopt, math, os, sys, time, re
import pandas as pd
import tensorflow as tf
import numpy as np
import time
import psutil
import platform

# tf.config.threading.set_inter_op_parallelism_threads(14)
# tf.config.threading.set_intra_op_parallelism_threads(2)


class TimeHistory(tf.keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.times = []

    def on_epoch_begin(self, epoch, logs={}):
        self.epoch_time_start = time.time()

    def on_epoch_end(self, epoch, logs={}):
        self.times.append(time.time() - self.epoch_time_start)            


res_df = pd.DataFrame(columns = [])
meta_data = {}

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


file_type=sys.argv[1]

file_name="/home/parallels/Documents/cheetah/examples/06-dnn-image/"
if file_type == "10k":
    file_name+="wiki_imdb_10k.pkl"
elif file_type == "1k":
    file_name+="wiki_imdb_1k.pkl"
elif file_type == "2k":
    file_name+="wiki_imdb_2k.pkl"
elif file_type == "5k":
    file_name+="wiki_imdb_5k.pkl"
elif file_type == "2h":
    file_name+="wiki_imdb_2h.pkl"
elif file_type == "4h":
    file_name+="wiki_imdb_4h.pkl"
else:
    file_name+="wiki_imdb_1h.pkl"
    

meta_data['file_type']=file_type

# get args
# model_name=sys.argv[2]

version=str(sys.argv[2])
CPU_GPU=sys.argv[3]

batch_size=int(sys.argv[4])
epochs=int(sys.argv[5])
learning_rate=float(sys.argv[6])
model_name=sys.argv[7]



meta_data['CPU_GPU']=CPU_GPU

#prepare datasets
img_height = 224
img_width = 224
img_depth = 3
img_shape = (img_height, img_width, img_depth)


train_df = pd.read_pickle(file_name)
ages_bins = train_df['age_class'].values
face_data = []
for i in range(0, train_df.shape[0]):
    face_data.append(train_df['pixels'].values[i])
del train_df
face_data = np.array(face_data)
face_data = face_data.reshape(face_data.shape[0], 224, 224, 3)
face_data = face_data/255.0


test_df = pd.read_pickle("/home/parallels/Documents/cheetah/examples/06-dnn-image/wiki_imdb_test.pkl")
t_ages_bins = test_df['age_class'].values
t_face_data = []
for i in range(0, test_df.shape[0]):
    t_face_data.append(test_df['pixels'].values[i])
del test_df
t_face_data = np.array(t_face_data)
t_face_data = t_face_data.reshape(t_face_data.shape[0], 224, 224, 3)
t_face_data = t_face_data/255.0


batch_sizes_list = [32]
if batch_sizes_list[len(batch_sizes_list)-1] < len(ages_bins):
    append_val = len(ages_bins)
    batch_sizes_list.append(append_val)
epochs_list = [2]
learning_rate_list = [0.001]


# batch_sizes_list = [10, 50]
# while batch_sizes_list[len(batch_sizes_list)-1] < len(ages_bins):
#     append_val = batch_sizes_list[len(batch_sizes_list)-1] * 2
#     batch_sizes_list.append(append_val)
# epochs_list = [1]
# learning_rate_list = [0.001]

# models_list=['vgg16', 'resnet', 'inception']
models_list=['vgg16']

meta_data['model_name']=model_name
meta_data['batch_size']=batch_size
meta_data['epochs']=epochs
meta_data['learning_rate']=learning_rate
meta_data['FP16']=0
print("** (b, e, lr)",batch_size, epochs, learning_rate)

if model_name == "resnet":
    model_n = tf.keras.applications.resnet50.ResNet50(input_shape=img_shape, weights=None, include_top=False)
elif model_name == "inception":
    model_n = tf.keras.applications.inception_v3.InceptionV3(input_shape=img_shape, weights=None, include_top=False)
else:
    model_n = tf.keras.applications.vgg16.VGG16(input_shape=img_shape, weights=None, include_top=False)
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(10, activation='softmax')
model = tf.keras.Sequential([
    model_n,
    global_average_layer,
    prediction_layer
])
opt = tf.keras.optimizers.Adam(learning_rate=learning_rate)
model.compile(optimizer=opt,
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            metrics=['accuracy'])
            
time_callback = TimeHistory()

fit_start = time.perf_counter()
#model.fit(x=face_data, y=ages_bins, batch_size=batch_size, epochs=epochs, workers=28, use_multiprocessing=True, callbacks=[time_callback])
model.fit(x=face_data, y=ages_bins, batch_size=batch_size, epochs=epochs, callbacks=[time_callback])
fit_end = time.perf_counter();
fit_time = fit_end - fit_start

str_time = [str(round(i, 2)) for i in time_callback.times]
times_rounds=[round(i, 2) for i in time_callback.times]
epochs_times = ';'.join(str_time)
epochs_times_one=times_rounds[0]
epochs_times_avg=sum(times_rounds)/len(times_rounds)

meta_data['epochs_times']=epochs_times
meta_data['epochs_times_one']=epochs_times_one
meta_data['epochs_times_avg']=epochs_times_avg

test_loss, test_acc = model.evaluate(x=t_face_data, y=t_ages_bins, verbose=2)
print("************************************************", test_acc, "---", str_time)
meta_data['test_accuracy']=round(test_acc,4)
meta_data['fit_time']=round(fit_time, 2)

print("** (b, e, lr, et)",batch_size, epochs, learning_rate, epochs_times)

r_df = pd.DataFrame([meta_data])
res_df = res_df.append(r_df)

print("RESULT", res_df)

print("MODEL ACCURACY ON TEST:",round(test_acc,4))
print("MODEL FIT ON TEST:",round(fit_time, 2))

cur_dir = os.path.basename(os.path.normpath(tmp_dir))
meta_data['run_config']=cur_dir
res_file_name = 'codar.post.details.'+cur_dir+'.csv'
# res_file_name = 'DNNs_c'+str(meta_data['sys_tot_cores_count'])+'_s'+file_type+'_v'+version+'.csv'
res_df.to_csv(res_file_name, header=True, index=False)





