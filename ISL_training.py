''' This interface sends Unix commands to run In-Silico Labeling TensorFlow program (Christiansen et al 2018). There are two modes: Predicting and Training. This one is for Training.
'''

import subprocess
import argparse
import os
import sys
# sys.path.append('/finkbeiner/imaging/smb-robodata/Sina/ISL_Scripts/')
sys.path.append('/mnt/finkbeinernas/robodata/Sina/')
import configure
from datetime import datetime
from time import strftime
import tempfile
import cv2
import numpy as np

global temp_directory, dataset_training

def image_feeder(dataset_training):

	global BG_WELL_DICT
	# input_image_stack_list, BG_WELL_DICT = background_removal_mp.get_image_tokens_list(INPUT_PATH, ROBO_NUMBER, IMAGING_MODE, VALID_WELLS, VALID_TIMEPOINTS, BG_WELL)

	# get channels
	# channels = set([x[0][4] for x in image_stack_list])

	# get rows and columns
	# rows = background_removal_mp.natural_sort(set([re.search(r'[A-P]', x).group(0) for x in VALID_WELLS]))
	# columns = background_removal_mp.natural_sort(set([re.search(r'\d{1,2}', x).group(0) for x in VALID_WELLS]))

  # build list of wells in the imaging order (i.e. snaking across the plate)
	wells_ordered = []
	# for r in rows:
	# 	for c in columns:
	# 		well = r + c
	# 		if any(well in x for x in VALID_WELLS):
	# 			wells_ordered.extend([well])
	# 			columns = list(reversed(columns))

  # reorder image list by imaging order so that batches contain neighboring wells
	# image_stack_list.sort(key=lambda x:sum(wells_ordered.index(i[3]) for i in x))

	# for ch in channels:
	# 	for tp in VALID_TIMEPOINTS:
	# 		# subset list by images from current channel and timepoint
	# 		image_stack_list_ch = [[tokens for tokens in montage if tokens[4] == ch if tokens[5] == tp] for montage in image_stack_list]

			# remove empty lists for non-matching channels (couldn't figure out how to do it in the above list comprehension)
			# image_stack_list_ch = [x for x in image_stack_list_ch if x]


			# if os.path.exists(temp_directory):
			# 	os.mkdir(os.path.join(output_path,temp_directory))
			# 	assert os.path.exists(temp_directory), 'Path to input images.'
			# with os.scandir(dataset_training) as location:
	temp_directory = tempfile.mkdtemp()
	print('The created Temp Directory is: ', temp_directory,'\n')
	print(temp_directory)
	print('\n',os.listdir(configure.dataset_training),'\n')

	for entry in os.listdir(configure.dataset_training):
		if entry.find('B3')>= 0 :
			dataset_location = os.path.join(configure.dataset_training, entry)
			# print (dataset_location)
			tmp_location = os.path.join(temp_directory,'B3')
			print(tmp_location)
			os.popen('cp -r '+dataset_location+' '+ str(temp_directory)+';')
			image = [np.zeros((2048,2048),np.uint16)]*375
			path = ''
			k=0
			New_file_name = []
			# print('\n',dataset_location)
			for img in os.listdir(dataset_location):
				# print(img)
				if img.find('.tif')>=0:
					path = str(os.path.join(dataset_location, img))
					image[k] = cv2.imread(path,-1)
					# print(image[k])
					base = os.path.splitext(img)[0]
					New_file_name= str(tmp_location)+'/'+base+'.png'
					image[k] = cv2.imwrite(New_file_name,image[k])
					# print(New_file_name)
					k+=1
				else:
					continue

		elif entry.find('E4')>=0:
			dataset_location = os.path.join(configure.dataset_training, entry)
			# print (dataset_location)
			tmp_location = os.path.join(temp_directory,'E4')
			print(tmp_location)
			os.popen('cp -r '+dataset_location+' '+ str(temp_directory)+';')
			image = [np.zeros((2048,2048),np.uint16)]*375
			path = ''
			k=0
			New_file_name = []
			# print('\n',dataset_location)
			for img in os.listdir(dataset_location):
				# print(img)
				if img.find('.tif')>=0:
					path = str(os.path.join(dataset_location, img))
					image[k] = cv2.imread(path,-1)
					# print(image[k])
					base = os.path.splitext(img)[0]
					New_file_name= str(tmp_location)+'/'+base+'.png'
					image[k] = cv2.imwrite(New_file_name,image[k])
					# print(New_file_name)
					k+=1
				else:
					continue

		elif entry.find('G2')>=0:
			dataset_location = os.path.join(configure.dataset_training, entry)
			# print (dataset_location)
			tmp_location = os.path.join(temp_directory,'G2')
			print(tmp_location)
			os.popen('cp -r '+dataset_location+' '+ str(temp_directory)+';')
			image = [np.zeros((2048,2048),np.uint16)]*375
			path = ''
			k=0
			New_file_name = []
			# print('\n',dataset_location)
			for img in os.listdir(dataset_location):
				# print(img)
				if img.find('.tif')>=0:
					path = str(os.path.join(dataset_location, img))
					image[k] = cv2.imread(path,-1)
					# print(image[k])
					base = os.path.splitext(img)[0]
					New_file_name= str(tmp_location)+'/'+base+'.png'
					image[k] = cv2.imwrite(New_file_name,image[k])
					# print(New_file_name)
					k+=1
				else:
					continue

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

	#Making sure the Bazel program has been shutdown properly.
	base_directory_path = 'cd '+ configure.base_directory + '; '
	# cmd1 = [base_directory_path + 'bazel shutdown;']
	# process1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
	# process1.wait()
	temp_directory = image_feeder(configure.dataset_prediction)

	print('\n',temp_directory,'\n')

	# Loop through subfolders in the dataset folder

	for folder in os.listdir(configure.dataset_prediction):

		# use re.match
		if (str('B3') or str('E4') or str('G2')) in folder:
			#Running Bazel for Training. Note txt log files are also being created incase troubleshooting is needed.
			print("Bazel Launching")

			# The directory where the checkpoints in 'train' subfolder will be saved.
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
			> ' + output_path + '/training_output_'+ date_time +'_B2images.txt \
			2> ' + output_path + '/training_error_'+ date_time +'_B2images.txt;']

			process2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
			process2.wait()

			print("Bazel Shutdown")

			#Here we shutdown the Bazel program.
			cmd3 = [base_directory_path + 'bazel shutdown;']
			process3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
			process3.wait()
		else:
			continue

			return

	## Launch tensorboard disabled for cluster.
	# cmd2 = ['tensorboard --logdir /home/sinadabiri/venvs/in-silico-labeling-master/isl']
	# process2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
	# process2.wait()
	# output2 = process2.communicate()[0]

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
  parser.add_argument("outfile", help="Folder path to images directory.")
  args = parser.parse_args()
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

