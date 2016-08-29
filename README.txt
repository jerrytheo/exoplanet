====================================================================================================

 _________                         _______     __                                        __
|         |                       |        \  |  |                                      |  |
|   ______|                       |   ___   \ |  |                                 _____|  |_______
|  |                              |  |   \   ||  |                                 \____    ______/
|  |___      __     __   ______   |  |___/   ||  |    _____  _    __  ____     ______   |  |
|      |    |  |   |  | /  __  \  |         / |  |   /  __ \| |  |  |/    \   /  __  \  |  |
|   ___|     \  \ /  / |  /  \  | |   _____/  |  |  |  /  \   |  |         | /  /__|  | |  |
|  |          \  /  /  | |    | | |  |        |  |  | |    |  |  |    __   ||   _____/  |  |
|  |______   /  /\  \  | |    | | |  |        |  |  | |    |  |  |  /   |  ||  |        |  |
|         | /  /  \  \ |  \__/  | |  |        |  |__|  \__/   |__|  |   |  | \  \_____  |  |__
|_________||__|    |__| \______/  |__|        |____/ \______/|__/|__|   |__|  \_______| |____/
 __________________________________________________________________________________________________
|__________________________________________________________________________________________________|

                                                                    
====================================================================================================


ExoPlanet v1.0                                                                       August 19, 2016
~~~~~~~~~~~~~~                                                                       ~~~~~~~~~~~~~~~


====================================================================================================



                                    Process - Project - Predict
                                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

ExoPlanet is a graphical desktop application built to ease out the procedure of running common
machine learning algorithms on a dataset through the use of a page and form based user interface.
We have designed the application centered around three stages: Processing Data, Projecting Results,
and Predicting Patterns; all of which are performed on an object called the Workspace.

         ________________________________________________________________________________
        |                                                                                |
        |                                    WORKSPACE                                   |
        |                                    ---------                                   |
        |                                                                                |
        |                                 ________________                               |
        |                                |                |                              |
        |              |---------------->|  Process Data  |                              |
        |              |                 |________________|                              |
        |              |                         |                                       |
        |              |                         |                                       |
        |              |                         |                                       |
        |              |                         |                                       |
        |              |                         |                                       |
        |              |                         |                                       |
        |              |                         |                                       |
        |              |                         |                                       |
        |         _____|_____________            |            ____________________       |
        |        |                   |           |           |                    |      |
        |        |  Project Results  |<----------|---------->|  Predict Patterns  |      |
        |        |___________________|                       |____________________|      |
        |                                                                                |
        |________________________________________________________________________________|


Workspace Entities
========= ========

A Workspace consists of three major entities:

1. Dataset: The data to process in tabular form.
    
    Each row pertains to a single sample of the data and each column being one feature of the
    sample. It is read from a specified comma-separated values (csv) file and stored as a matrix in
    memory. The dataset may or may not have associated labels, which, if present, are also read from
    a csv file (separate from the data file).

2. Model: An abstract system trained to identify patterns in data.
    
    The training, or analysis of data, can be supervised or unsupervised (Clustering) based on the
    nature of the dataset. Supervised training may be with respect to continuous (Regression) or
    discrete (Classification) labels.

3. Visuals: A visual representation of the Model's performance.
    
    These results are presented using graphs or tables.


Workspace Stages
========= ======

Process Data Stage
------- ---- -----
At this stage the Model is trained to fit the Dataset using the algorithm selected. The range of
algorithms available depend on the nature of the Dataset (no labels, continuous labels or discrete
labels). The parameters of the algorithm can be adjusted pretraining or after viewing the
Projected Results.

Project Results Stage
------- ------- -----
Before the Process Data stage, the Dataset can be split into 3 separate sets called the Training
set, the Validating set and the Testing set. The Training set is used to train the Model, while the
Validating set and the Testing set can be used to build the Visuals.

Since the first instance of Model training may yield unsatisfactory results, one can always go back
to the Process Data Stage and either change the algorithm itself or alter the parameters of the same
algorithm.

Predict Patterns Stage
------- -------- -----
At the final stage the trained Model is used to predict the occurences of similar patterns in a new
Dataset, provided the structure of the new Dataset is identical to the original Dataset.


====================================================================================================


                                        Instructions for Use
                                        ~~~~~~~~~~~~~~~~~~~~

Creating a Workspace:
1.  Pick a name for the Workspace.
        ->  The name must begin with an alphabet.
        ->  The name can only contain alphanumeric characters and underscores.
2.  Select the type of analysis to perform.
3.  Select the algorithm to train on.
    Select the data file (and label file, if present) and the delimiter and set whether headers are
    present.
    Set the sizes of each set.
4.  Adjust the parameters of the algorithm if required and/or needed and click Start to initiate
    training.

Once training is complete, you have the option to either Evaluate the results of training or use
the Model to predict labels for new data. If the analysis type is clustering, you can also save
the cluster labels of the data.

Evaluating, Adjusting and Recreating the Model:
1.  Select the set to build visuals on (selecting both concatenates the sets) and click Evaluate.
2.  Click Save Workspace to save the Workspace to disk.
        ->  The Data is saved along with the Workspace.
3.  Click Save Visuals to save the graphs as Portable Network Graphics (png) files and Tables in csv
    files.
4.  Click Change Parameters to go back to the Parameters page, and adjust the required values.
    Click Start to recreate the Model.
5.  Click Back at the Change Parameters page to go one step further back to change the algorithm of
    training.

Predict Labels:
1.  Select the file to read new data from.
        ->  The structure of the data must be identical to the original data (same features).
    Select the delimiter and set whether headers present.
    Click Predict.
2.  To save the current labels, click Save Labels. A prompt appears.
        ->  Selecting Yes appends the new data and its corresponding labels to the original data
            file and labels file.
        ->  Selecting No creates a new file for the new data's labels.


====================================================================================================

                                            Dependencies
                                            ~~~~~~~~~~~~


Package                     Download and/or Installation Instructions
-------                     -------- ------ ------------ ------------
Scikit Learn, 0.17.1        http://scikit-learn.org/stable/install.html
PyQt 4.11.4,                https://www.riverbankcomputing.com/software/pyqt/download


====================================================================================================

                                              License
                                              ~~~~~~~

                Copyright (C) 2016  Abhijit J. Theophilus, Mohinish L. Reddy

                This program is free software: you can redistribute it and/or modify
                it under the terms of the GNU General Public License as published by
                the Free Software Foundation, either version 3 of the License, or
                (at your option) any later version.

                This program is distributed in the hope that it will be useful,
                but WITHOUT ANY WARRANTY; without even the implied warranty of
                MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
                GNU General Public License for more details.

                You should have received a copy of the GNU General Public License
                along with this program.  If not, see <http://www.gnu.org/licenses/>.


====================================================================================================

                                              Authors
                                              ~~~~~~~

                        Abhijit Jeremiel Theophilus        abhitheo96@gmail.com      
                           Mohinish Lokesh Reddy        mohinishlokesh96@gmail.com


====================================================================================================