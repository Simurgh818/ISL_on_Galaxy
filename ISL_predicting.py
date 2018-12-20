''' This interface sends Unix commands to run In-Silico Labeling TensorFlow program (Christiansen et al 2018). This script is to run prediction on multiple images.
'''

import subprocess
import argparse, pickle, os, sys, shutil
sys.path.append('/mnt/finkbeinernas/robodata/Sina/')
import configure
# sys.path.append('/home/sinadabiri/galaxy-neuron-analysis/galaxy/tools/dev_staging_modules')
# import utils
# from background_removal_mp import get_image_token_list
from datetime import datetime
from time import strftime
import tempfile
import cv2
import numpy as np

global temp_directory, dataset_prediction
# temp_directory = '/home/sinadabiri/galaxy-new2/galaxy/database/tmp/'

INPUT_PATH = ''
ROBO_NUMBER = None
IMAGING_MODE = ''
VALID_WELLS = []
VALID_TIMEPOINTS = []

def image_feeder(dataset_prediction):

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
			# with os.scandir(dataset_prediction) as location:

	temp_directory = tempfile.mkdtemp()
	print('The created Temp Directory is: ', temp_directory,'\n')
	print(temp_directory)
	print('\n',os.listdir(configure.dataset_prediction),'\n')

	for entry in os.listdir(configure.dataset_prediction):
		if entry.find('G11')>= 0 :
			dataset_location = os.path.join(configure.dataset_prediction, entry)
			# print (dataset_location)
			tmp_location = os.path.join(temp_directory,'G11')
			os.mkdir(tmp_location)
			print(tmp_location)
			# tmp_location is better
			# os.popen('cp -r '+ dataset_location+ ' ' + str(tmp_location)+';')
			image = [np.zeros((2048,2048),np.int16)]*5
			path = ''
			k=0
			New_file_name = []
			# print('\n',dataset_location)
			for img in os.listdir(dataset_location):
				print(img)
				# if img.find('_BRIGHTFIELD_')>=0:
				# 	os.popen('cp '+dataset_location+'/'+img+' ' + str(tmp_location)+'/'+img+';')
				path = str(os.path.join(dataset_location, img))
				tmp_location_img = str(os.path.join(tmp_location, img))
				if img.find('.tif')>=0:
					image[k] = cv2.imread(path,cv2.IMREAD_ANYDEPTH)
					# print(image[k])
					base = os.path.splitext(img)[0]
					New_file_name= str(tmp_location)+'/'+base+'.png'
					# path = os.rename(path, New_file_name)
					# os.popen('mv '+path+' '+ New_file_name+';')
					image[k] = cv2.imwrite(New_file_name,image[k])
					# print(New_file_name)
					k+=1
				else:
					os.popen('cp '+path+' ' + tmp_location_img+';')


		elif entry.find('C2')>=0:
			dataset_location = os.path.join(configure.dataset_prediction, entry)
			# print (dataset_location)
			tmp_location = os.path.join(temp_directory,'C2')
			os.mkdir(tmp_location)
			print(tmp_location)
			# os.popen('cp -r '+ dataset_location+ ' ' + str(tmp_location)+';')
			image = [np.zeros((2048,2048),np.int16)]*5
			path = ''
			k=0
			New_file_name = []
			# print('\n',dataset_location)
			for img in os.listdir(dataset_location):
				# print(img)
				# if img.find('_BRIGHTFIELD_')>=0:
				# 	os.popen('cp '+dataset_location+'/'+img+ ' ' + str(tmp_location)+';')
				if img.find('.tif')>=0:
					path = str(os.path.join(dataset_location, img))
					image[k] = cv2.imread(path,cv2.IMREAD_ANYDEPTH)
					# print(image[k])
					base = os.path.splitext(img)[0]
					New_file_name= str(tmp_location)+'/'+base+'.png'
					image[k] = cv2.imwrite(New_file_name,image[k])
					# print(New_file_name)
					k+=1
				else:
					os.popen('cp '+path+' ' + tmp_location_img+';')

		elif entry.find('E7')>=0:
			dataset_location = os.path.join(configure.dataset_prediction, entry)
			# print (dataset_location)
			tmp_location = os.path.join(temp_directory,'E7')
			os.mkdir(tmp_location)
			print(tmp_location)
			# os.popen('cp -r '+ dataset_location+ ' ' + str(tmp_location)+';')
			image = [np.zeros((2048,2048),np.int16)]*5
			path = ''
			k=0
			New_file_name = []
			# print('\n',dataset_location)
			for img in os.listdir(dataset_location):
				# print(img)
				# if img.find('_BRIGHTFIELD_')>=0:
				# 	os.popen('cp '+dataset_location+'/'+img+ ' ' + str(tmp_location)+';')
				if img.find('.tif')>=0:
					path = str(os.path.join(dataset_location, img))
					image[k] = cv2.imread(path,cv2.IMREAD_ANYDEPTH)
					# print(image[k])
					base = os.path.splitext(img)[0]
					New_file_name= str(tmp_location)+'/'+base+'.png'
					image[k] = cv2.imwrite(New_file_name,image[k])
					# os.popen('mv '+path+' '+ New_file_name+';')
					# print(New_file_name)
					k+=1
				else:
					os.popen('cp '+path+' ' + tmp_location_img+';')

	print('\n',"The temporary directory subfolders are: ", os.listdir(temp_directory),'\n')
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
	print("var_dict: ", var_dict, '\n')


  # ----Initialize parameters------------------
	# bg_well = str.strip(args.chosen_bg_well) if args.chosen_bg_well else None

	crop_size = args.crop_size
	model_location = args.model_location
	output_path = args.output_path
	dataset_eval_path = args.dataset_eval_path
	infer_channels = args.infer_channels
	# outfile = args.outfile
	pickle.dump(var_dict, open('var_dict.p', 'wb'))
	# outfile = shutil.move('var_dict.p', outfile)

	INPUT_PATH = args.dataset_eval_path
	OUTPUT_PATH = args.output_path

	# BG_WELL = bg_well
	# ROBO_NUMBER = int(var_dict['RoboNumber'])
	# IMAGING_MODE = var_dict['ImagingMode']
	VALID_WELLS = var_dict['Wells']
	VALID_TIMEPOINTS = var_dict['TimePoints']

	print("VALID_WELLS: ", VALID_WELLS, '\n')
	print("VALID_TIMEPOINTS: ", VALID_TIMEPOINTS, '\n')

	if model_location != '':
		model_location = '--restore_directory ' + configure.model_location
		mod = 'ISL-Model'
	else:
		model_location = ''
		mod = 'Your-Model'

	# ----Confirm given folders exist--
	if not os.path.exists(dataset_eval_path):
		print('Confirm the given path to input images (transmitted images used to generate prediction image) exists.')
		assert os.path.exists(dataset_eval_path), 'Path to input images (transmitted images used to generate prediction image).'
		if not os.path.exists(output_path):
			print('Confirm the given path to output of prediction for fluorescent and validation images exists.')

			assert os.path.abspath(output_path) != os.path.abspath(dataset_eval_path) , 'Please provide a unique data path.'
			assert os.path.abspath(output_path) != os.path.abspath(model_location),  'Please provide a unique model path.'

			date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")

			print('\n The Evaluation Directory is:')
			print(dataset_eval_path)
			print('\n The Output Directory is:')
			print(output_path)
			print('\n ')

		# temp_directory = image_feeder(configure.dataset_prediction)
	#Making sure the Bazel program has been shutdown properly.
	base_directory_path = 'cd '+ configure.base_directory + '; '
	# cmd1 = [base_directory_path + 'bazel version;']
	# process1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
	# process1.wait()
	temp_directory = image_feeder(configure.dataset_prediction)

	print('\n',temp_directory,'\n')

	# Loop through subfolders in the dataset folder

	for folder in os.listdir(temp_directory):

		# use re.match
		if folder.find('')>=0:
			#Running Bazel for prediction. Note txt log files are also being created incase troubleshooting is needed.
			date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")
			dataset_eval_path = str(os.path.join(temp_directory, folder))
			print("Dataset Eval Path is: ",dataset_eval_path,'\n')

			print("Bazel Launching", '\n')

			base_dir = 'export BASE_DIRECTORY=' + configure.base_directory + '/isl;  '

			baz_cmd = [base_directory_path + base_dir + 'bazel run isl:launch -- \
			--alsologtostderr \
			--base_directory $BASE_DIRECTORY \
			--mode EVAL_EVAL \
			--metric INFER_FULL \
			--stitch_crop_size '+ crop_size + ' \
			--restore_directory '+ configure.model_location + ' \
			--output_path '+ output_path + ' \
			--read_pngs \
			--dataset_eval_directory ' + dataset_eval_path + ' \
			--infer_channel_whitelist ' + infer_channels + ' \
			--error_panels False \
			--infer_simplify_error_panels \
			> ' + OUTPUT_PATH + '/predicting_output_'+ mod + '_'+ date_time +'_'+ crop_size +'_'+ folder + '_images.txt \
			2> ' + OUTPUT_PATH + '/predicting_error_'+ mod + '_'+ date_time +'_'+ crop_size + '_'+ folder + '_images.txt;']

			process = subprocess.Popen(baz_cmd, shell=True, stdout=subprocess.PIPE)
			process.wait()

			print("Bazel Shutdown")

			#Here we shutdown the Bazel program.
			cmd3 = [base_directory_path + 'bazel shutdown;']
			process3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
			process3.wait()
		else:
			continue

			return



if __name__ == '__main__':

	main()

	# ----Output for user and save dict----------

	# Save dict to file
	# pickle.dump(var_dict, open(outfile, 'wb'))


