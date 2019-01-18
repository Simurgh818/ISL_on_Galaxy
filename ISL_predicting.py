''' This interface sends Unix commands to run In-Silico Labeling TensorFlow program (Christiansen et al 2018). This script is to run prediction on multiple images.
'''

import subprocess
import argparse, pickle, os, sys, shutil
from datetime import datetime
from time import strftime
import tempfile
import cv2
import numpy as np

global temp_directory, tmp_location, dataset_prediction, VALID_WELLS, VALID_TIMEPOINTS,dataset_eval_path


INPUT_PATH = ''
ROBO_NUMBER = None
IMAGING_MODE = ''
VALID_WELLS = []
VALID_TIMEPOINTS = []
tmp_location = ''
tmp_location_img = ''

def image_feeder(dataset_prediction, valid_wells, valid_timepoints):

	temp_directory = tempfile.mkdtemp(dir = output_path)

	print('The subfolders in dataset_prediction folder are: ',os.listdir(dataset_eval_path),'\n')
	print("VALID_WELLS: ", VALID_WELLS, '\n')
	print("VALID_TIMEPOINTS: ", VALID_TIMEPOINTS, '\n')
	print('The created Temp Directory is: ', temp_directory,'\n')


	for entry in VALID_WELLS:
		if entry.find('')>= 0 :
			dataset_location = os.path.join(dataset_eval_path, entry)
			tmp_location = os.path.join(temp_directory,entry)
			if not os.path.exists(tmp_location):
				os.mkdir(tmp_location)

			image = [np.zeros((2048,2048),np.int16)]*15
			path = ''
			k=0
			New_file_name = []
			for img in os.listdir(dataset_location):
				path = str(os.path.join(dataset_location, img))
				time_point = os.path.basename(img).split('_')[2]
				for tp in VALID_TIMEPOINTS:
					if (img.endswith('.tif')>=0 and time_point==tp):
						image[k] = cv2.imread(path,cv2.IMREAD_ANYDEPTH)
						tmp_location_tp = os.path.join(tmp_location,tp)
						if not os.path.exists(tmp_location_tp):
							os.mkdir(tmp_location_tp)
						tmp_location_img = str(os.path.join(tmp_location_tp, img))

						base = os.path.splitext(img)[0]
						New_file_name= str(tmp_location_tp)+'/'+base+'.png'
						image[k] = cv2.imwrite(New_file_name,image[k])
						k+=1
					elif time_point==tp:
						tmp_location_tp = os.path.join(tmp_location,tp)
						if not os.path.exists(tmp_location_tp):
							os.mkdir(tmp_location_tp)
						tmp_location_img = str(os.path.join(tmp_location_tp, img))
						os.popen('cp '+path+' ' + tmp_location_img+';')

	return temp_directory;

def main():
	""" First the script makes sure the Bazel has been shutdown properly. Then it starts the bazel command with the following arguments:

	Args:
	crop_size: the image crop size the user chose the prediction to be done for.
	model_location: wheter the user wants to use the model that has been trained before in the program, or use their own trained model.
	output_path: The location where the folder (eval_eval_infer) containing the prediction image will be stored at.
	dataset_eval_path: The location where the images to be used for prediction are sotred at.
	infer_channels: The microscope inference channels.

	"""

	base_directory_path = 'cd '+ base_directory + '; '

	for w in os.listdir(temp_directory):
		date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")
		print("We are on well: ",w)
		if (w.find('G11'))>=0:
			dataset_eval_path_w = str(os.path.join(temp_directory, w))
			print("dataset_eval_path_w is: ",dataset_eval_path_w, '\n')
			print('\n','The temp_directory subfolders are: ',os.listdir(dataset_eval_path_w),'\n')

			for tp in os.listdir(dataset_eval_path_w):
				if tp.find('T0')>=0:
					dataset_eval_path_tp = str(os.path.join(dataset_eval_path_w, tp))

			#Running Bazel for prediction. Note txt log files are also being created incase troubleshooting is needed.
					date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")
					dataset_eval_path = dataset_eval_path_tp
					print("Dataset Eval Path is: ",dataset_eval_path_tp,'\n')
					print("Inference channels are: ", infer_channels)
					print("Bazel Launching--------------------------------------------", '\n')

					base_dir = 'export BASE_DIRECTORY=' + base_directory + '/isl;  '

					baz_cmd = [base_directory_path + base_dir + 'bazel run isl:launch -- \
					--alsologtostderr \
					--base_directory $BASE_DIRECTORY \
					--mode EVAL_EVAL \
					--metric INFER_FULL \
					--stitch_crop_size '+ crop_size + ' \
					--restore_directory '+ model_location + ' \
					--output_path '+ output_path + ' \
					--read_pngs \
					--dataset_eval_directory ' + dataset_eval_path_tp + ' \
					--infer_channel_whitelist ' + infer_channels + ' \
					--error_panels False \
					--infer_simplify_error_panels \
					> ' + output_path + '/predicting_output_'+ mod + '_'+ date_time +'_'+
					crop_size +'_'+ w +'_'+ tp +'_images.txt \
					2> ' + output_path + '/predicting_error_'+ mod + '_'+ date_time +'_'+
					crop_size + '_'+ w + '_'+ tp +'_images.txt;']
						# '_'+ tp +
					process = subprocess.Popen(baz_cmd, shell=True, stdout=subprocess.PIPE)
					process.wait()

	# Here we delete the temp folder.
	print("temp_directory is going to be removed: ",temp_directory)
	cmd3 = ['rm -r ' + temp_directory + ';']
	process3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
	process3.wait()

	return



if __name__ == '__main__':
	#Receiving the variables from the XML script, parse them, initialize them, and verify the paths exist.

	# ----Parser-----------------------
	parser = argparse.ArgumentParser(description="ISL Predicting.")
	parser.add_argument("infile", help="Load input variable dictionary")
	parser.add_argument("crop_size", help="Image Crop Size.")
	parser.add_argument("model_location", help="Model Location.")
	parser.add_argument("output_path", help="Output Image Folder location.")
	parser.add_argument("dataset_eval_path", help="Folder path to images directory.")
	parser.add_argument("infer_channels", help="Channel Inferences.")
	# parser.add_argument("outfile", help="Name of output dictionary.")
	args = parser.parse_args()

	# ----Load path dict-------------------------
	infile = args.infile
	var_dict = pickle.load(open(infile, 'rb'))

  # ----Initialize parameters------------------
	crop_size = args.crop_size
	base_directory = '/home/sinadabiri/venvs/in-silico-labeling-master'
	model_location = args.model_location
	output_path = args.output_path
	dataset_eval_path = args.dataset_eval_path
	infer_channels = args.infer_channels
	# outfile = args.outfile
	pickle.dump(var_dict, open('var_dict.p', 'wb'))
	# outfile = shutil.move('var_dict.p', outfile)

	INPUT_PATH = args.dataset_eval_path



	VALID_WELLS = var_dict['Wells']
	VALID_TIMEPOINTS = var_dict['TimePoints']

	if model_location != '':
		mod = 'ISL-Model'
	else:
		model_location = ''
		mod = 'Your-Model'

	temp_directory = image_feeder(dataset_eval_path, VALID_WELLS, VALID_TIMEPOINTS)

	# ----Confirm given folders exist--
	if not os.path.exists(dataset_eval_path):
		print('Confirm the given path to input images (transmitted images used to generate prediction image) exists.')
		assert os.path.exists(dataset_eval_path), 'Path to input images used to generate prediction image is wrong.'
		if not os.path.exists(output_path):
			print('Confirm the given path to output of prediction for fluorescent and validation images exists.')

			assert os.path.abspath(output_path) != os.path.abspath(dataset_eval_path) , 'Please provide a unique data path.'
			assert os.path.abspath(output_path) != os.path.abspath(model_location),  'Please provide a unique model path.'

			date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")

			print('\n The Evaluation Directory is: ', dataset_eval_path)
			print('\n The Output Directory is: ',output_path)
			print('\n ')


	main()

	# ----Output for user and save dict----------

	# Save dict to file
	# pickle.dump(var_dict, open(outfile, 'wb'))


