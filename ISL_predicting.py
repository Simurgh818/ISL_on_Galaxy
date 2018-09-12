import subprocess
import argparse
import sys, os
from datetime import datetime
from time import strftime

dataset_eval_dir = ' '
output_dir = ' '


def main():

	# ~/venvs/tensorflow/SinaFlow/bin/activate
	# virtual_env_path_active = 'source ~/venvs/tensorflow/SinaFlow/bin/activate;  '
	
	# /home/sinadabiri/venvs/in-silico-labeling-master
	base_directory_path = 'cd /home/sinadabiri/venvs/in-silico-labeling-master; '

	cmd1 = [base_directory_path + 'bazel shutdown;']
	process1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
	process1.wait()

	base_dir = 'export BASE_DIRECTORY=/mnt/finkbeinernas/robodata/Sina/in-silico-labeling/isl;  '
	

	baz_cmd = [base_directory_path + base_dir + 'bazel run isl:launch -- \
	  --alsologtostderr \
	  --base_directory $BASE_DIRECTORY \
	  --mode EVAL_EVAL \
	  --metric INFER_FULL \
	  --stitch_crop_size '+ image_crop_size + ' ' +  model_type +' \
	  --output_path '+ output_dir + ' \
	  --read_pngs \
	  --dataset_eval_directory ' + dataset_eval_dir + '  \
	  --infer_channel_whitelist ' + infer_chan + ' \
	  --infer_simplify_error_panels \
    > ' + output_dir + '/predicting_output_'+ mod + '_'+ date_time +'_'+ image_crop_size +'_condition_b_sample_images.txt \
    2> ' + output_dir + '/predicting_error_'+ mod + '_'+ date_time +'_'+ image_crop_size +'_condition_b_sample_images.txt;']
	
	process = subprocess.Popen(baz_cmd, shell=True, stdout=subprocess.PIPE)
	process.wait()
	output = process.communicate()[0]

	cmd3 = [base_directory_path + 'bazel shutdown;']
	process3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
	process3.wait()

	return 


if __name__ == '__main__':
  
  # ----Parser-----------------------
	parser = argparse.ArgumentParser(description="ISL Predicting.")
	parser.add_argument("crop_size", help="Image Crop Size.")
	parser.add_argument("model", help="Model type.")
	parser.add_argument("output_path", help="Output Image Folder location.")
	parser.add_argument("dataset_eval_path", help="Folder path to images directory.")
	parser.add_argument("infer_channels", help="Channel Inferences.")

	args = parser.parse_args()

  # ----Initialize parameters------------------

	image_crop_size = args.crop_size
	model_type = args.model
	output_dir = args.output_path
	dataset_eval_dir = args.dataset_eval_path
	infer_chan = args.infer_channels

	if model_type != '':
		model_type = '--restore_directory /home/sinadabiri/venvs/in-silico-labeling-master/isl/checkpoints'
		mod = 'ISL-Model'
	else:
		model_type = ''
		mod = 'Your-Model'
	
	# ----Confirm given folders exist--

	assert os.path.exists(dataset_eval_dir), 'Confirm the given path for images directory exists.'
	assert os.path.exists(output_dir), 'Confirm the given path for output images directory exists.'

	date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")

	print ('\n The Evaluation Directory is:')
	print (dataset_eval_dir)
	print ('\n The Output Directory is:')
	print (output_dir)
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


