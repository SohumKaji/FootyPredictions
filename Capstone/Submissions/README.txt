READ ME
-------
This project has all of the data required included in the submission folder. 
Each of the .ipynb files is correctly setup to use the provided data. No set up is needed.


                 Table of Contents
----------------------------------------------------------
SGDClassifier            | SGDClassifier.ipynb           |
NerualNetwork            | NeuralNet.ipynb               |
Fulltime: Random Forests | Random_Forests_fulltime.ipynb |
Fulltime: PCA            | PCA_fulltime.ipynb            |
Halftime: Random Forests | Random_Forests_halftime.ipynb |
Halftime: PCA            | PCA_halftime.ipynb            |
----------------------------------------------------------

For each of these files, if you only want to view the output, you can take a look at the associated .html files for each.


Packages: Tensorflow, Pandas, Numpy, Sklearn, matplotlib

Each of these libraries is fairly standard. 
Tensorflow is for the neural network. 
Pandas is to work with dataframes.
Numpy is to work with ndarrays.
Sklearn is to implement Random Forets, PCA, and the SGDClassifier
matplotlib is to create the graphics you see in the report and in the jupyter notebook files


I have included the Selenium scripts for you viewing pleasure. They are unnecessary to get the project to work considering the data has been provided.

If you would like to collect the data for this project by yourself:

I have included the selenium scripts that I used, however, they may or may not work at this moment as the format of the websites they are meant to function on have changed 
(I collected some of this data as early as in July).

You will need to download Chromedriver and Google Chrome as well as install Selenium to use these files.
Simply open each of the three files: DC_schedule.py, DC_halftime.py, DC_fulltime.py and replace the path_to_chromedriver variable with the path to your chromedriver.
Then run each of these three files. Then run convert_for_sgd-final.py.

Then you will have all of the data required for this project. The collection process takes a few hours and takes control of a Chrome window on your device for this duration.