import subprocess
import argparse
import sys, os
import datetime

DatasetEvalDir = ' '

def main():

	# ~/venvs/tensorflow/SinaFlow/bin/activate
	VirtualEnvPathActive = 'source ~/venvs/tensorflow/SinaFlow/bin/activate;'
	# /home/sinadabiri/venvs/in-silico-labeling-master
	BaseDirectoryPath = 'cd /home/sinadabiri/venvs/in-silico-labeling-master;'
	
	cmd1 = [VirtualEnvPathActive + BaseDirectoryPath + 'bazel shutdown; export BASE_DIRECTORY=/mnt/finkbeinernas/robodata/Sina/in-silico-labeling/isl; bazel run isl:launch -- \
	  --alsologtostderr \
	  --base_directory $BASE_DIRECTORY \
	  --mode TRAIN \
	  --metric LOSS \
	  --master "" \
	  --restore_directory '+ CheckpointDir + ' \
	  --output_directory '+ OutputDir + ' \
	  --read_pngs \
	  --dataset_train_directory ' + DatasetTrainDir + ' \
    > ' + OutputDir + '/training_output_'+ Date +'_B2images.txt \
    2> ' + OutputDir + '/training_error_'+ Date +'_B2images.txt']

	process1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
	process1.wait()
	output1 = process1.communicate()[0]

	#Step 7.1: check the loss graphs to see how our model is training 

	cmd2 = ['tensorboard --logdir /home/sinadabiri/venvs/in-silico-labeling-master/isl']
	process2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
	process2.wait()
	output2 = process2.communicate()[0]
	
	print ("The Output Directory is:")
	print (OutputDir)
	print ("The Link to TensorBoard is:")
	print (output2)

	return output2


if __name__ == '__main__':
  
  # ----Parser-----------------------
	parser = argparse.ArgumentParser(description="ISL Testing.")
	parser.add_argument("DatasetTrainPath", help="Folder path to images directory.")
	parser.add_argument("CheckpointPath", help="Folder path to checkpoint directory.")
	parser.add_argument("OutputPath", help="Output Image Folder location.")
	parser.add_argument("outfile", help="Folder path to images directory.")
	args = parser.parse_args()

  # ----Initialize parameters------------------
	DatasetTrainDir = args.DatasetTrainPath
	CheckpointDir = args.CheckpointPath
	OutputDir = args.OutputPath
	outfile = args.outfile

	# ----Confirm given folders exist--
	assert os.path.exists(DatasetTrainDir), 'Confirm the given path for images directory exists.'
	assert os.path.exists(CheckpointDir), 'Confirm the given path for images directory exists.'
	assert os.path.exists(OutputDir), 'Confirm the given path for output images directory exists.'
	
	Date = str(datetime.date.today())
	
	main()

