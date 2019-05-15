''' This interface sends Unix commands to run In-Silico Labeling TensorFlow program (Christiansen et al 2018). This script is to run prediction on multiple images.
'''

import subprocess
import argparse, pickle, os, shutil
from datetime import datetime
import cv2
import numpy as np
import configure

global temp_directory, tmp_location, dataset_prediction, VALID_WELLS, VALID_TIMEPOINTS, dataset_eval_path

INPUT_PATH = ''
ROBO_NUMBER = None
IMAGING_MODE = ''
# loop_iterations_row = 0
# loop_iterations_col = 0

def image_feeder(dataset_prediction, valid_wells, valid_timepoints):
    temp_directory = os.path.join(output_path, 'temp_directory')
    if not os.path.exists(temp_directory):
        os.mkdir(temp_directory)

    print('The subfolders in dataset_prediction folder are: ', os.listdir(dataset_eval_path), '\n')
    print("VALID_WELLS: ", VALID_WELLS, '\n')
    print("VALID_TIMEPOINTS: ", VALID_TIMEPOINTS, '\n')
    print('The created Temp Directory is: ', temp_directory, '\n')

    # For our dataset the following loop should be: for entry in VALID_WELLS: instead.
    for entry in VALID_WELLS:
        # os.listdir(dataset_eval_path)

        dataset_location = os.path.join(dataset_eval_path, entry)
        tmp_location = os.path.join(temp_directory, entry)
        if not os.path.exists(tmp_location):
            os.mkdir(tmp_location)

        k = 0

        for img in os.listdir(dataset_location):

            path = str(os.path.join(dataset_location, img))
            if len(os.path.basename(img).split('_')) >= 2:
                time_point = os.path.basename(img).split('_')[2]
            else:
                time_point = ''
            # print("The time point is: ",time_point)
            row, col = cv2.imread(path, cv2.IMREAD_ANYDEPTH).shape
            image = [np.zeros((row, col), np.int16)] * len(os.listdir(dataset_location))
            print('input image dimensions are row x col: ', row, ' x ', col)
            for tp in VALID_TIMEPOINTS:
                if (img.endswith('.tif') >= 0 and time_point == tp):
                    # and os.path.basename(img).split('_')[6].find('BRIGHTFIELD')>=0

                    image[k] = cv2.imread(path, cv2.IMREAD_ANYDEPTH)
                    #cv2.IMREAD_ANYDEPTH
                    if img.find('MAXPROJECT') > 0:
                        image[k] = image[k] - np.mean(image[k])
                        # cv2.equalizeHist(image[k], dst= cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
                    tmp_location_tp = os.path.join(tmp_location, tp)
                    if not os.path.exists(tmp_location_tp):
                        os.mkdir(tmp_location_tp)

                    base = os.path.splitext(img)[0]
                    New_file_name = str(tmp_location_tp) + '/' + base + '.png'
                    image[k] = cv2.imwrite(New_file_name, image[k])
                    k += 1
                elif time_point == tp:
                    # and os.path.basename(img).split('_')[6].find('BRIGHTFIELD')>=0
                    tmp_location_tp = os.path.join(tmp_location, tp)
                    if not os.path.exists(tmp_location_tp):
                        os.mkdir(tmp_location_tp)
                    tmp_location_img = str(os.path.join(tmp_location_tp, img))
                    os.popen('cp ' + path + ' ' + tmp_location_img + ';')

        loop_iterations_row = round(row // int(crop_size))
        loop_iterations_col = round(col // int(crop_size))
        print('image row, col loop iterations are : ', loop_iterations_row, loop_iterations_col)

    return temp_directory, loop_iterations_col, loop_iterations_row


def main():
    """ First the script makes sure the Bazel has been shutdown properly. Then it starts the bazel command with the following arguments:

    Args:
    crop_size: the image crop size the user chose the prediction to be done for.
    model_location: wheter the user wants to use the model that has been trained before in the program, or use their own trained model.
    output_path: The location where the folder (eval_eval_infer) containing the prediction image will be stored at.
    dataset_eval_path: The location where the images to be used for prediction are sotred at.
    infer_channels: The microscope inference channels.

    """

    base_directory_path = 'cd ' + base_directory + '; '

    for w in VALID_WELLS:
        date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")
        print("We are on well: ", w)

        dataset_eval_path_w = str(os.path.join(temp_directory, w))
        print("dataset_eval_path_w is: ", dataset_eval_path_w, '\n')
        print('\n', 'The temp_directory subfolders are: ', os.listdir(dataset_eval_path_w), '\n')

        for tp in VALID_TIMEPOINTS:

            dataset_eval_path_tp = str(os.path.join(dataset_eval_path_w, tp))

            print("Dataset Eval Path is: ", dataset_eval_path_tp, '\n')
            print("Inference channels are: ", infer_channels)

            column_start = '0'

            print("loop_iteration_col is: ", loop_iterations_col)

            for col_tile in range(0, loop_iterations_col):
                print("we are on column: ", col_tile)
                row_start = '0'
                for row_tile in range(0, loop_iterations_row):
                    date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")
                    print("we are on row: ", row_tile)
                    print("row_start is set to: ", row_start)
                    # Running Bazel for prediction. Note txt log files are also being created
                    # in case troubleshooting is needed.

                    print("Bazel Launching------------------------", '\n')
                    base_dir = 'export BASE_DIRECTORY=' + base_directory + '/isl;  '
                    baz_cmd = [base_directory_path + base_dir + 'bazel run isl:launch -- \
                    --alsologtostderr \
                    --base_directory $BASE_DIRECTORY \
                    --mode EVAL_EVAL \
                    --metric INFER_FULL \
                    --stitch_crop_size ' + crop_size + ' \
                    --row_start ' + row_start + ' \
                    --column_start ' + column_start + ' \
                    --restore_directory ' + model_location + ' \
                    --output_path ' + output_path + ' \
                    --read_pngs \
                    --dataset_eval_directory ' + dataset_eval_path_tp + ' \
                    --infer_channel_whitelist ' + infer_channels + ' \
                    --error_panels False \
                    --infer_simplify_error_panels \
                    > ' + output_path + '/predicting_output_' + mod + '_' + date_time + '_' +
                    crop_size + '_' + w + '_' + tp + '_' + column_start + '-' + row_start +
                               '_images.txt \
                    2> ' + output_path + '/predicting_error_' + mod + '_' + date_time + '_' +
                    crop_size + '_' + w + '_' + tp + '_' + column_start + '-' + row_start +
                               '_images.txt;']

                    print('The baz_cmd is now: ', baz_cmd)
                    process = subprocess.Popen(baz_cmd, shell=True, stdout=subprocess.PIPE)
                    process.wait()
                    print("Bazel Finished=====================================================", '\n')
                    row_start = str(int(row_start) + int(crop_size))

                column_start = str(int(column_start) + int(crop_size))
                print("column_start is set to: ", column_start)

    # Here we delete the temp folder.
    print("temp_directory is going to be removed: ", temp_directory)
    cmd3 = ['rm -r ' + temp_directory + ';']
    process3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
    process3.wait()

    return


if __name__ == '__main__':
    # Receiving the variables from the XML script, parse them, initialize them, and verify the paths exist.

    # ----Parser-----------------------
    parser = argparse.ArgumentParser(description="ISL Predicting.")
    parser.add_argument("infile", help="Load input variable dictionary")
    parser.add_argument("crop_size", help="Image Crop Size.")
    parser.add_argument("model_location", help="Model Location.")
    parser.add_argument("output_path", help="Output Image Folder location.")
    parser.add_argument("dataset_eval_path", help="Folder path to images directory.")
    parser.add_argument("infer_channels", help="Channel Inferences.")
    parser.add_argument("outfile", help="Name of output dictionary.")
    args = parser.parse_args()

    # ----Load path dict-------------------------
    infile = args.infile
    var_dict = pickle.load(open(infile, 'rb'))

    # ----Initialize parameters------------------
    crop_size = args.crop_size
    print("The crop size is: ", crop_size)
    base_directory = configure.base_directory
    model_location = args.model_location
    print("The model location is: ", model_location)
    output_path = args.output_path
    print("The output path is: ", output_path)
    dataset_eval_path = args.dataset_eval_path
    print("The brightfield images are located at: ", dataset_eval_path)
    infer_channels = args.infer_channels
    print("The inference channels are: ", infer_channels)
    outfile = args.outfile
    pickle.dump(var_dict, open('var_dict.p', 'wb'))
    outfile = shutil.move('var_dict.p', outfile)

    INPUT_PATH = args.dataset_eval_path

    VALID_WELLS = var_dict['Wells']
    VALID_TIMEPOINTS = var_dict['TimePoints']

    if model_location != '':
        mod = 'ISL-Model'
    else:
        model_location = ''
        mod = 'Your-Model'

    temp_directory, loop_iterations_col, loop_iterations_row = \
        image_feeder(dataset_eval_path, VALID_WELLS, VALID_TIMEPOINTS)

    # ----Confirm given folders exist--
    if not os.path.exists(dataset_eval_path):
        print('Confirm the given path to input images (transmitted images used to generate prediction image) exists.')
        assert os.path.exists(dataset_eval_path), 'Path to input images used to generate prediction image is wrong.'
        if not os.path.exists(output_path):
            print('Confirm the given path to output of prediction for fluorescent and validation images exists.')

            assert os.path.abspath(output_path) != os.path.abspath(
                dataset_eval_path), 'Please provide a unique data path.'
            assert os.path.abspath(output_path) != os.path.abspath(
                model_location), 'Please provide a unique model path.'

            date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")

            print('\n The Evaluation Directory is: ', dataset_eval_path)
            print('\n The Output Directory is: ', output_path)
            print('\n ')

    main()

    # ----Output for user and save dict----------

    # Save dict to file
    pickle.dump(var_dict, open(outfile, 'wb'))
