import sys, os, pkgutil
import question1.Preprocessing as prep
import question1.CleanData as clean
import question1.DataVisualization as visual

import question2.NearestNeighbours as nn
import question2.NearestSubroutes as ns
import question2.MapInGridView as gv
import question2.JourneyClassification as jc
import utils
import random


def question_1(input_file, output_file, output_folder, maps_folder):
    # Question 1
    print(">>> Running question 1a - parsing the training data")
    trips_list = prep.question_1a(input_file, output_file)
    print(">>> Running question 1b - cleaning the training data")
    trips_list = clean.question_1b(output_folder, trips_list)
    print(">>> Running question 1b - visualizing the training data")
    visual.question_1c(maps_folder, trips_list)
    print("Finished question1")


def question_2(train_file, test_files, output_folder, maps_folder, paropts):
    # Question 2
    # Read the training data
    trips_list = utils.read_trips(train_file)
    print(">>> Running question 2a1 - Nearest neighbours computation")
    nn.question_a1(maps_folder, test_files[0], trips_list, paropts)
    print(">>> Running question 2a2 - Nearest subroutes computation")
    ns.question_a2(maps_folder, test_files[1], trips_list)
    print(">>> Running question 2b - Cell grid quantization")
    cellgrid = (4, 3)
    print("Using cell grid:", cellgrid)
    features_file = gv.subquestion_b(trips_list, cellgrid, output_folder)
    print(">>> Running question 2c - Classification")
    jc.question_c(features_file, output_folder)


def check_dependencies():
    deps = ['numpy', 'scipy']
    for dep in deps:
        res = pkgutil.find_loader(dep)
        if res is None:
            print("The python3 package [%s] is required to run." % dep)
            exit(1)
    if not os.path.exists('rasterize.js'):
        print("The rasterize.js tool from the phantomjs framework is required to run.")
        exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s inputfolder outputfolder" % sys.argv[0])
        exit(1)
    check_dependencies()
    print("Running %s with arguments: %s" % (os.path.basename(sys.argv[0]), sys.argv))
    input_folder  = os.path.abspath(sys.argv[1])
    output_folder = os.path.abspath(sys.argv[2])

    rand_seed = 123123
    random.seed(rand_seed)

    paropts = ("processes",8)

    # question 1
    ############

    # prepare files
    train_file = os.path.join(input_folder, "train_set.csv")
    output_file = os.path.join(output_folder, "trips.csv")
    output_file_clean = os.path.join(output_folder, "trips_clean.csv")
    maps_folder = os.path.join(output_folder, "gmplots")
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(maps_folder, exist_ok=True)

    # run
    # question_1(train_file, output_file, output_file_clean, maps_folder)

    # question 2
    ############

    # prepare files
    test_files = [ os.path.join(input_folder, "test_set_a%d.csv" % t) for t in [1,2]]

    # run
    question_2(output_file_clean, test_files, output_folder, maps_folder, paropts)
