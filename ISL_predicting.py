''' This interface sends Unix commands to run In-Silico Labeling TensorFlow program (Christiansen et al 2018). There are two modes: Predicting and Training. This one is for Predicting.
'''

import subprocess
import argparse
import os
import configure
from datetime import datetime
from time import strftime


def main():
	""" First the script makes sure the Bazel has been shutdown properly. Then it starts the bazel command with the following arguments:

	Args: 
	crop_size: the image crop size the user chose the prediction to be done for.
	model_location: wheter the user wants to use the model that has been trained before in the program, or use their own trained model.
	output_path: The location where the folder (eval_eval_infer) containing the prediction image will be stored at. 
	dataset_eval_path: The location where the images to be used for prediction are sotred at.
	infer_channels: The microscope inference channels.

	"""

	#Making sure the Bazel program has been shutdown properly.
	base_directory_path = 'cd '+ configure.base_directory + '; '
	# cmd1 = [base_directory_path + 'bazel version;']
	# process1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
	# process1.wait()

	#Running Bazel for prediction. Note txt log files are also being created incase troubleshooting is needed.
	print("Bazel Launching")

	base_dir = 'export BASE_DIRECTORY=' + configure.base_directory + '/isl;  '
	
	baz_cmd = [base_directory_path + base_dir + 'bazel run isl:launch -- \
	--alsologtostderr \
	--base_directory $BASE_DIRECTORY \
	--mode EVAL_EVAL \
	--metric INFER_FULL \
	--stitch_crop_size '+ crop_size + ' ' +  configure.model_location +' \
	--output_path '+ configure.output_path + ' \
	--read_pngs \
	--dataset_eval_directory ' + configure.dataset_prediction + '  \
	--infer_channel_whitelist ' + infer_channels + ' \
	--infer_simplify_error_panels \
	> ' + configure.output_path + '/predicting_output_'+ mod + '_'+ date_time +'_'+ crop_size +'_condition_b_sample_images.txt \
	2> ' + configure.output_path + '/predicting_error_'+ mod + '_'+ date_time +'_'+ crop_size +'_condition_b_sample_images.txt;']

	process = subprocess.Popen(baz_cmd, shell=True, stdout=subprocess.PIPE)
	process.wait()

	print("Bazel Shutdown")

	#Here we shutdown the Bazel program. 
	cmd3 = [base_directory_path + 'bazel shutdown;']
	process3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
	process3.wait()

	return 


if __name__ == '__main__':

  #Receiving the variables from the XML script, parse them, initialize them, and verify the paths exist. 
  
  # ----Parser-----------------------
	parser = argparse.ArgumentParser(description="ISL Predicting.")
	parser.add_argument("crop_size", help="Image Crop Size.")
	parser.add_argument("model_location", help="Model Location.")
	parser.add_argument("output_path", help="Output Image Folder location.")
	parser.add_argument("dataset_eval_path", help="Folder path to images directory.")
	parser.add_argument("infer_channels", help="Channel Inferences.")

	args = parser.parse_args()

  # ----Initialize parameters------------------
	crop_size = args.crop_size
	model_location = args.model_location
	output_path = args.output_path
	dataset_eval_path = args.dataset_eval_path
	infer_channels = args.infer_channels

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
	elif (args.output_path==args.dataset_eval_path or args.output_path==args.model_location):
		print ('Confirm the given path to output train directory is different than dataset or checkpoint paths.')
		assert os.path.exists(output_path), 'Path to output of prediction for fluorescent and validation images.'

	date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")

	print('\n The Evaluation Directory is:')
	print(dataset_eval_path)
	print('\n The Output Directory is:')
	print(output_path)
	print('\n ')

	main()


