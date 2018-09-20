# Notes
- Two models `./models/green.h5` and `./models/red.h5`
- Both drive great on track 1, 2, 3, and 4 for more than 8 laps consistently and without too much wobble
- Works with app `formula-trend-1.0.0-alpha.5`

# SETUP

- Install [Anaconda](https://www.continuum.io/downloads) or [Miniconda](https://conda.io/miniconda.html)
- Create environment
```
#Use TensorFlow without GPU
$ conda env create -f ./misc/environments.yml

#Use TensorFlow with GPU
$ conda env create -f ./misc/environment-gpu.yml

# conda install -c anaconda keras-gpu
# conda install keras
```

# Unify Data
- Maked directories to put your images
```
$ pwd
/Users/mithi/Desktop/repos/little-miss-trendy/A-AV2
$ mkdir ./road-images-2/red-flat
$ mkdir ./road-images-2/green-flat

```
- Run to put all images from subdirectories to one directory
```
$ find ./road-images-2/red/ -name '*.jpg' -exec cp '{}' ./road-images-2/red-flat/ \;
$ find ./road-images-2/green/ -name '*.jpg' -exec cp '{}' ./road-images-2/green-flat/ \;
```
- Run script to merge all log csv files to one csv file
```
$ ruby ./misc/process-merge-csvs.rb ./PATH/TO/CSV/LOGS /PATH/TO/IMAGES /PATH/TO/FINAL/CSV/
$ ruby ./misc/process-merge-csvs.rb ./road-images-2/green/ ./road-images-2/green-flat/ ./road-images-2/green.csv
$ ruby ./misc/process-merge-csvs.rb ./road-images-2/red/ ./road-images-2/red-flat/ ./road-images-2/red.csv
```

# Analyze data, train and save model
- Activate environment and run Jupyter
```
# for mac
$ source activate trendy
$ Jupyter notebook
```
- Inspect the data using `A-DATA-INSPECTION.ipynb`
- Train and save your model using `A-MODEL-SAMPLE.ipynb`

# Run your app and model
- Run your app
```
$ pwd
/Users/mithi/Desktop/DONOTBACKUP/apps/formula-trend-1.0.0-alpha.5/Mac/formula-trend-1.0.0-alpha.5.app/Contents
$ ./MacOS/formula-trend-1.0.0-alpha.5

$ pwd
/Users/mithi/Desktop/DONOTBACKUP/apps/formula-trend-1.0.0-beta.3/Mac/formula-trend-1.0.0-beta.3.app/Contents/MacOS
$ ./formula-trend-1.0.0-beta.3
```

9. Run your agent either with model green.h5 or red.h5

```
$ python drive.py ./models/green.h5
$ python drive.py ./models/red.h5

```
