''' This interface sends Unix commands to run In-Silico Labeling TensorFlow program (Christiansen et al 2018). There are two modes: Predicting and Training. This one is for Training.
'''

import subprocess
import argparse
import sys, os
from datetime import datetime
from time import strftime


def main():
	""" First the script makes sure the Bazel has been shutdown properly. Then it starts the bazel command with the following arguments:

	Args: 
	dataset_train_path: Folder path to images directory to be used for training.
	checkpoint_path: Folder path to where the checkpoints of the ISL model is stored. 
	output_path: Folder path to where the train subdirectory, that contains the checkpoints will be saved.  
	until_step: The upper step number limit for training. 
	
	"""

	#Making sure the Bazel program has been shutdown properly.
	base_directory_path = 'cd /finkbeiner/imaging/home/in-silico/in-silico-labeling; '
	cmd1 = [base_directory_path + 'bazel shutdown;']
	process1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
	process1.wait()

	#Running Bazel for Training. Note txt log files are also being created in case troubleshooting is needed.

	# The directory where the checkpoints in 'train' subfolder will be saved.
	base_dir = 'export BASE_DIRECTORY=/finkbeiner/imaging/home/in-silico/in-silico-labeling/isl; '
	cmd2 = [base_directory_path + base_dir + 'bazel run isl:launch -- \
	  --alsologtostderr \
	  --base_directory $BASE_DIRECTORY \
	  --mode TRAIN \
	  --metric LOSS \
	  --master "" \
	  --restore_directory '+ checkpoint_path + ' \
	  --output_path '+ output_path + ' \
	  --read_pngs \
	  --dataset_train_directory ' + dataset_train_path + ' \
	  --until_step ' + until_step + ' \
    > ' + output_path + '/training_output_'+ date_time +'_B2images.txt \
    2> ' + output_path + '/training_error_'+ date_time +'_B2images.txt;']

	process2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
	process2.wait()

	#Here we shutdown the Bazel program.
	cmd3 = [base_directory_path + 'bazel shutdown;']
	process3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
	process3.wait()

	## Launch tensorboard disabled for cluster.
	# cmd2 = ['tensorboard --logdir /home/sinadabiri/venvs/in-silico-labeling-master/isl']
	# process2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
	# process2.wait()
	# output2 = process2.communicate()[0]
	
	print ("Model checkpoints are written to:")
	print (output_path)
	# print ("The Link to TensorBoard is:")
	# print (output2)

	# return output2


if __name__ == '__main__':
  
  #Receiving the variables from the XML script, parse them, initialize them, and verify the paths exist. 
  
  # ----Parser-----------------------
	parser = argparse.ArgumentParser(description="ISL Testing.")
	parser.add_argument("dataset_train_path", help="Folder path to images directory.")
	parser.add_argument("checkpoint_path", help="Folder path to checkpoint directory.")
	parser.add_argument("output_path", help="Output 'train' Folder location, where checkpoints will be saved.")
	parser.add_argument("until_step", help="Train till step number mentioned.")
	parser.add_argument("outfile", help="Folder path to images directory.")
	args = parser.parse_args()

  # ----Initialize parameters------------------
	dataset_train_path = args.dataset_train_path
	checkpoint_path = args.checkpoint_path
	output_path = args.output_path
	until_step = args.until_step
	outfile = args.outfile

	# ----Confirm given folders exist--
	if not os.path.exists(dataset_train_path):
	    print 'Confirm the given path to input images (transmitted images used for training) exists.'
	assert os.path.exists(dataset_train_path), 'Confirm the given path for training images directory exists.'
	if not os.path.exists(checkpoint_path):
	    print 'Confirm the given path to checkpoints directory exists.'
	assert os.path.exists(checkpoint_path), 'Confirm the given path for checkpoints directory exists.'
	if not os.path.exists(output_path):
	    print 'Confirm the given path to output train directory (where new checkpoints will be saved) exists.'
	assert os.path.exists(output_path), 'Confirm the given path for output train directory (where new checkpoints will be saved) exists.'
	
	date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")
	
	main()

