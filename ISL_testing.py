import subprocess
import argparse
import sys, os
from datetime import datetime
from time import strftime

DatasetEvalDir = ' '
OutputDir = ' '


def main():

	# ~/venvs/tensorflow/SinaFlow/bin/activate
	VirtualEnvPathActive = 'source ~/venvs/tensorflow/SinaFlow/bin/activate; '
	
	# /home/sinadabiri/venvs/in-silico-labeling-master
	BaseDirectoryPath = 'cd /home/sinadabiri/venvs/in-silico-labeling-master; '
	
	cmd1 = [BaseDirectoryPath + 'bazel shutdown;']
	process1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
	process1.wait()

	BaseDir = 'export BASE_DIRECTORY=/mnt/finkbeinernas/robodata/Sina/in-silico-labeling/isl; '
	
	# VirtualEnvPathActive.append ('bazel run isl:launch-- \
	BazCmd = [VirtualEnvPathActive + BaseDirectoryPath + BaseDir + 'bazel run isl:launch -- \
	  --alsologtostderr \
	  --base_directory $BASE_DIRECTORY \
	  --mode EVAL_EVAL \
	  --metric INFER_FULL \
	  --stitch_crop_size '+ ImageCropSize + ' ' + Modeltype +' \
	  --output_directory '+ OutputDir + ' \
	  --read_pngs \
	  --dataset_eval_directory ' + DatasetEvalDir + '  \
	  --infer_channel_whitelist ' + InferChan + ' \
	  > ' + OutputDir + '/testing_output_'+ Mod + '_'+ DateTime +'_'+ ImageCropSize +'_condition_b_sample_images.txt \
    2> ' + OutputDir + '/testing_error_'+ Mod + '_'+ DateTime +'_'+ ImageCropSize +'_condition_b_sample_images.txt;']
	
	process = subprocess.Popen(BazCmd, shell=True, stdout=subprocess.PIPE)
	process.wait()
	output = process.communicate()[0]

	cmd3 = [BaseDirectoryPath + 'bazel shutdown;']
	process3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
	process3.wait()
	return 


if __name__ == '__main__':
  
  # ----Parser-----------------------
	parser = argparse.ArgumentParser(description="ISL Testing.")
	parser.add_argument("CropSize", help="Image Crop Size.")
	parser.add_argument("Model", help="Model type.")
	parser.add_argument("OutputPath", help="Output Image Folder location.")
	parser.add_argument("DatasetEvalPath", help="Folder path to images directory.")
	parser.add_argument("InferChannels", help="Channel Inferences.")

	args = parser.parse_args()

  # ----Initialize parameters------------------

	ImageCropSize = args.CropSize
	Modeltype = args.Model
	Mod = args.Model
	OutputDir = args.OutputPath
	DatasetEvalDir = args.DatasetEvalPath
	InferChan = args.InferChannels

	if Modeltype == 'Pre-trained':
		Modeltype = '--restore_directory /home/sinadabiri/venvs/in-silico-labeling-master/isl/checkpoints'
	else:
		Modeltype = ' '
	
	# ----Confirm given folders exist--

	assert os.path.exists(DatasetEvalDir), 'Confirm the given path for images directory exists.'
	assert os.path.exists(OutputDir), 'Confirm the given path for output images directory exists.'

	DateTime = datetime.now().strftime("%m-%d-%Y_%H:%M")

	print ('\n The Evaluation Directory is:')
	print (DatasetEvalDir)
	print ('\n The Output Directory is:')
	print (OutputDir)
	print ('\n ')
	# # Confirm given folders exist
	# if not os.path.exists(input_path):
	#     print 'Confirm the given path for data exists.'
	# assert os.path.exists(input_path), 'Confirm the given path for data exists.'
	# if not os.path.exists(output_path):
	#     print 'Confirm the given path for results exists.'
	# assert os.path.exists(output_path), 'Confirm the given path for results exists.'
	# assert input_path != output_path, 'With new well subdirectory requirement, output destination must be different than input.'

	main()


