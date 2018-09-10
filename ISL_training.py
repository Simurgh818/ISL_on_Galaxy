import subprocess
import argparse
import sys, os
from datetime import datetime
from time import strftime


def main():

	# ~/venvs/tensorflow/SinaFlow/bin/activate
	# virtual_env_path_active = 'source ~/venvs/tensorflow/SinaFlow/bin/activate;'

	# /home/sinadabiri/venvs/in-silico-labeling-master
	base_directory_path = 'cd /home/sinadabiri/venvs/in-silico-labeling-master; '
	
	cmd1 = [base_directory_path + 'bazel shutdown;']
	process1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
	process1.wait()

	# The directory where the checkpoints and output prediction image will be saved at.
	base_dir = 'export BASE_DIRECTORY=/mnt/finkbeinernas/robodata/Sina/in-silico-labeling/isl; '
	
	cmd2 = [virtual_env_path_active + base_directory_path + base_dir + 'bazel run isl:launch -- \
	  --alsologtostderr \
	  --base_directory $BASE_DIRECTORY \
	  --mode TRAIN \
	  --metric LOSS \
	  --master "" \
	  --restore_directory '+ checkpoint_dir + ' \
	  --output_path '+ output_dir + ' \
	  --read_pngs \
	  --dataset_train_directory ' + dataset_train_dir + ' \
	  --until_step ' + till_step + ' \
    > ' + output_dir + '/training_output_'+ date_time +'_B2images.txt \
    2> ' + output_dir + '/training_error_'+ date_time +'_B2images.txt;']

	process2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
	process2.wait()
	output2 = process1.communicate()[0]

	cmd3 = [base_directory_path + 'bazel shutdown;']
	process3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
	process3.wait()

	#check the loss graphs to see how our model is training 

	# cmd2 = ['tensorboard --logdir /home/sinadabiri/venvs/in-silico-labeling-master/isl']
	# process2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
	# process2.wait()
	# output2 = process2.communicate()[0]
	
	print ("The Output Directory is:")
	print (output_dir)
	# print ("The Link to TensorBoard is:")
	# print (output2)

	# return output2


if __name__ == '__main__':
  
  # ----Parser-----------------------
	parser = argparse.ArgumentParser(description="ISL Testing.")
	parser.add_argument("dataset_train_path", help="Folder path to images directory.")
	parser.add_argument("checkpoint_path", help="Folder path to checkpoint directory.")
	parser.add_argument("output_path", help="Output Image Folder location.")
	parser.add_argument("till_step", help="Train till step number mentioned.")
	parser.add_argument("outfile", help="Folder path to images directory.")
	args = parser.parse_args()

  # ----Initialize parameters------------------
	dataset_train_dir = args.dataset_train_path
	checkpoint_dir = args.checkpoint_path
	output_dir = args.output_path
	till_step = args.till_step
	outfile = args.outfile

	# ----Confirm given folders exist--
	assert os.path.exists(dataset_train_dir), 'Confirm the given path for images directory exists.'
	assert os.path.exists(checkpoint_dir), 'Confirm the given path for images directory exists.'
	assert os.path.exists(output_dir), 'Confirm the given path for output images directory exists.'
	
	date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")
	
	main()

