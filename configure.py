''' This interface sends Unix commands to run In-Silico Labeling TensorFlow program (Christiansen et al 2018). There are two modes: Predicting and Training. This script is to set the paths for virtual environment to run the programs, the path to checkpoints, image dataset, and output folder.
'''
'''This configuration is for Sina's computer '''
# /finkbeiner/imaging/smb-robodata/Sina

virtual_environment = '/home/sinadabiri/venvs/tensorflow/SinaFlow/bin/activate'
base_directory = '/home/sinadabiri/venvs/in-silico-labeling-master'
model_location = '/mnt/finkbeinernas/robodata/Sina/checkpoints'
# output_path = '/mnt/finkbeinernas/robodata/Sina/LogFiles'
# dataset_prediction = '/mnt/finkbeinernas/robodata/Sina/data_sample/condition_b_sample'
dataset_training = '/mnt/finkbeinernas/robodata/Sina/data_sample/condition_e_sample_B2'

'''This part is for Server '''
# virtual_environment = '/finkbeiner/imaging/home/fbgalaxy/.virtualenvs/insilico/bin/activate'
# base_directory = '/finkbeiner/imaging/home/in-silico/in-silico-labeling/'
# model_location = '/finkbeiner/imaging/home/in-silico/checkpoints'
# output_path = '/finkbeiner/imaging/smb-robodata/Sina/LogFiles'
# dataset_prediction = '/finkbeiner/imaging/home/in-silico/datasets/condition_b_sample'
# dataset_training = '/finkbeiner/imaging/home/in-silico/datasets/condition_e_sample_B2'
