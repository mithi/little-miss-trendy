# Notes
- Two models `./models/green.h5` and `./models/red.h5`
- Both drive great on track 1, 2, 3, and 4 for more than 8 laps consistently and without too much wobble
- Works with app `formula-trend-1.0.0-alpha.5`

# SETUP

1. Install [Anaconda](https://www.continuum.io/downloads) or [Miniconda](https://conda.io/miniconda.html)
2. Create environment
```
#Use TensorFlow without GPU
$ conda env create -f ./misc/environments.yml

#Use TensorFlow with GPU
$ conda env create -f ./misc/environment-gpu.yml
```
3. Activate environment and run Jupyter

```
# for mac
$ source activate trendy
$ Jupyter notebook

# for pc
$ activate trendy
$ jupyter notebook
```
4. Run to put all images from subdirectories to one directory
```
$ find ./road-images/red/ -name '*.jpg' -exec cp '{}' ./road-images/red-flat/ \;
$ find ./road-images/green/ -name '*.jpg' -exec cp '{}' ./road-images/green-flat/ \;
```
5. Run script to merge all log csv files to one csv file
```
$ ruby ./misc/process-merge-csvs.rb ./road-images/green/ ./road-images/green-flat/ ./road-images/green.csv
$ ruby ./misc/process-merge-csvs.rb ./road-images/red/ ./road-images/red-flat/ ./road-images/red.csv
```

6. Inspect the data at `A-DATA-INSPECTION.ipynb`
7. Train and save your model at `A-MODEL-SAMPLE.ipynb`
8. Run your app
```
$ pwd
/Users/mithi/Desktop/DONOTBACKUP/apps/formula-trend-1.0.0-alpha.5/Mac/formula-trend-1.0.0-alpha.5.app/Contents

$ ./MacOS/formula-trend-1.0.0-alpha.5
``

9. Run your agent either with model `green.h5` or `red.h5`
```
$ python drive.py ./models/green.h5
$ python drive.py ./models/red.h5

```
