''' This interface sends Unix commands to run In-Silico Labeling TensorFlow program (Christiansen et al 2018). There are two modes: Predicting and Training. This script is to set the paths for virtual environment to run the programs, the path to checkpoints, image dataset, and output folder.
'''
import platform
import os
import xml.etree.ElementTree as ET

def main():
	tree = ET.parse ('ISL_predicting.xml')
	root = tree.getroot()

	for elem in root.iter('param')
		if name =="model_location":
			pass elem.set('value', check_points)
		

	return virtual_environment, check_points, output_path, dataset_prediction, dataset_training;




if __name__ == '__main__':

	virtual_environment = '/home/sinadabiri/venvs/tensorflow/SinaFlow/bin/activate'
	check_points = '/home/sinadabiri/venvs/in-silico-labeling-master/isl/checkpoints'
	output_path = '/home/sinadabiri/venvs/in-silico-labeling-master/LogFiles'
	dataset_prediction = '/home/sinadabiri/venvs/in-silico-labeling-master/isl/data_sample/condition_b_sample'
	dataset_training = '/home/sinadabiri/Testing-In-Silico-Labeling/data_sample/condition_e_sample_B2'

	# ----Confirm given folders exist--
	if not os.path.exists(virtual_environment):
	    print('Confirm the given path to the virtual environment exists.')
	assert os.path.exists(virtual_environment), 'Path to the virtual environment.'
	
	if not os.path.exists(check_points):
	    print('Confirm the given path to the checkpoints folder exists.'	)
	assert os.path.exists(check_points), 'Path to the checkpoints folder.'

	if not os.path.exists(output_path):
	    print('Confirm the given path to output of prediction for fluorescent and validation images exists.'	)
	assert os.path.exists(output_path), 'Path to output of prediction for fluorescent and validation images.'
	
	if not os.path.exists(dataset_prediction):
	    print('Confirm the given path to the dataset for prediction images exists.'	)
	assert os.path.exists(dataset_prediction), 'Path to dataset for prediction images.'
	
	if not os.path.exists(dataset_training):
	    print('Confirm the given path to the training dataset images exists.'	)
	assert os.path.exists(dataset_training), 'Path to training dataset images.'
	main()