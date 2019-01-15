''' This interface sends Unix commands to run In-Silico Labeling TensorFlow program (Christiansen et al 2018). There are two modes: Predicting and Training. This one is for Training.
'''

import subprocess
import argparse, pickle, os, sys
# sys.path.append('/finkbeiner/imaging/smb-robodata/Sina/ISL_Scripts/')
sys.path.append('/mnt/finkbeinernas/robodata/Sina/')
import configure
from datetime import datetime
from time import strftime
import tempfile
import cv2
import numpy as np

global temp_directory, dataset_training, VALID_WELLS, VALID_TIMEPOINTS

VALID_WELLS = []
VALID_TIMEPOINTS = []
tmp_location = ''

def image_feeder(dataset_training, valid_wells, valid_timepoints):

	temp_directory = tempfile.mkdtemp()
	print('The created Temp Directory is: ', temp_directory,'\n')
	print('The subfolders in dataset_training folder are: ',os.listdir(configure.dataset_training),'\n')
	print("VALID_WELLS: ", VALID_WELLS, '\n')
	print("VALID_TIMEPOINTS: ", VALID_TIMEPOINTS, '\n')

	for entry in VALID_WELLS:
		if entry.find('')>= 0 :
			dataset_location = os.path.join(configure.dataset_training, entry)
			tmp_location = os.path.join(temp_directory,entry)
			if not os.path.exists(tmp_location):
				os.mkdir(tmp_location)

			image = [np.zeros((2048,2048),np.int16)]*15
			path = ''
			k=0
			New_file_name = []


			for img in os.listdir(dataset_location):
				path = str(os.path.join(dataset_location, img))

				for tp in VALID_TIMEPOINTS:
					if (img.find('.tif')>=0 and img.find(tp)>=0):
						image[k] = cv2.imread(path,cv2.IMREAD_ANYDEPTH)
						# print(image[k])
						tmp_location_tp = os.path.join(tmp_location,tp)
						if not os.path.exists(tmp_location_tp):
							os.mkdir(tmp_location_tp)
						# print(tmp_location_tp)
						tmp_location_img = str(os.path.join(tmp_location_tp, img))

						base = os.path.splitext(img)[0]
						New_file_name= str(tmp_location_tp)+'/'+base+'.png'
						image[k] = cv2.imwrite(New_file_name,image[k])
						k+=1
					elif img.find(tp)>=0:
						tmp_location_tp = os.path.join(tmp_location,tp)
						if not os.path.exists(tmp_location_tp):
							os.mkdir(tmp_location_tp)
						tmp_location_img = str(os.path.join(tmp_location_tp, img))
						os.popen('cp '+path+' ' + tmp_location_img+';')



	print('\n',"The temporary directory subfolders are: ", os.listdir(temp_directory),'\n')
	return temp_directory;

def main():
	""" First the script makes sure the Bazel has been shutdown properly. Then it starts the bazel command with the following arguments:

	Args:
	dataset_train_path: Folder path to images directory to be used for training.
	model_location: Folder path to where the checkpoints of the ISL model is stored.
	output_path: Folder path to where the train subdirectory, that contains the checkpoints will be saved.
	until_step: The upper step number limit for training.

	"""


	base_directory_path = 'cd '+ configure.base_directory + '; '

	temp_directory = image_feeder(configure.dataset_training, VALID_WELLS, VALID_TIMEPOINTS)

	print('\n','The temp_directory: ',temp_directory,'\n')


	for folder in os.listdir(configure.dataset_training):

		# Loop through subfolders in the dataset folder
		for w in os.listdir(temp_directory):
			date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")
			print(w)
			if (w.find('G11'))>=0:
				dataset_train_path_w = str(os.path.join(temp_directory, w))
				print(dataset_train_path_w, '\n')
				print('\n','The temp_directory subfolders are: ',os.listdir(dataset_train_path_w),'\n')

				for tp in os.listdir(dataset_train_path_w):
					print(tp)
					print('The temp_directory',dataset_train_path_w)
					if tp.find('T0')>=0:
						dataset_train_path_tp = str(os.path.join(dataset_train_path_w, tp))
						print(dataset_train_path_tp, '\n')

						date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")
						dataset_train_path = dataset_train_path_tp

						print("Dataset Train Path is: ",dataset_train_path_tp,'\n')

						print("Bazel Launching")

						base_dir = 'export BASE_DIRECTORY=' + configure.base_directory + '/isl; '

						cmd2 = [base_directory_path + base_dir + 'bazel run isl:launch -- \
						--alsologtostderr \
						--base_directory $BASE_DIRECTORY \
						--mode TRAIN \
						--metric LOSS \
						--master "" \
						--restore_directory '+ configure.model_location + ' \
						--output_path '+ output_path + ' \
						--read_pngs \
						--dataset_train_directory ' + dataset_train_path + ' \
						--until_step ' + until_step + ' \
						> ' + output_path + '/training_output_'+ date_time + '_'+ w + '_'+ tp +'_images.txt \
						2> ' + output_path + '/training_error_'+ date_time + '_'+ w + '_'+ tp +'_images.txt;']

						process2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
						process2.wait()

			else:
				continue

			return

	print("Model checkpoints are written to:")
	print(output_path)
	# print ("The Link to TensorBoard is:")
	# print (output2)

	# return output2


if __name__ == '__main__':
  #Receiving the variables from the XML script, parse them, initialize them, and verify the paths exist.

	# ----Parser-----------------------
	parser = argparse.ArgumentParser(description="ISL Testing.")
	parser.add_argument("input_dict", help="Load input variable dictionary")
	parser.add_argument("dataset_train_path", help="Folder path to images directory.")
	parser.add_argument("model_location", help="Folder path to checkpoint directory.")
	parser.add_argument("output_path", help="Output 'train' Folder location, where checkpoints will be saved.")
	parser.add_argument("until_step", help="Train till step number mentioned.")
	parser.add_argument("outfile", help="Name of output dictionary.")
	args = parser.parse_args()


	# ----Load path dict-------------------------
	infile = args.input_dict
	var_dict = pickle.load(open(infile, 'rb'))

	# ----Initialize parameters------------------
	dataset_train_path = args.dataset_train_path
	model_location = args.model_location
	output_path = args.output_path
	until_step = args.until_step
	outfile = args.outfile

	VALID_WELLS = var_dict['Wells']
	VALID_TIMEPOINTS = var_dict['TimePoints']

	# ----Confirm given folders exist--
	if not os.path.exists(dataset_train_path):
		print ('Confirm the given path to input images (transmitted images used for training) exists.')
		assert os.path.exists(dataset_train_path), 'Confirm the given path for training images directory exists.'
		if not os.path.exists(model_location):
			print ('Confirm the given path to checkpoints directory exists.')
			assert os.path.exists(model_location), 'Confirm the given path for checkpoints directory exists.'
			if not os.path.exists(output_path):
				print ('Confirm the given path to output train directory (where new checkpoints will be saved) exists.')

				assert os.path.abspath(output_path) != os.path.abspath(dataset_train_path) ,  'Please provide unique output path  (not model or data path).'
				assert os.path.abspath(output_path) != os.path.abspath(model_location),  'Please provide unique output path  (not model or data path).'

				date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")
	main()

