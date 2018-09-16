# little-miss-trendy
- See each directory readme for more details

## Directory `./A-AV1/`
- Contains behavioral cloning work to to make a car run autonomously on app `formula-trend-1.0.0-alpha.4`

### Videos 
- [alpha4 track1](https://github.com/mithi/little-miss-trendy/blob/master/A-AV1/videos/track1-480p.mp4)
- [alpha4 track2](https://github.com/mithi/little-miss-trendy/blob/master/A-AV1/videos/track2-480p.mp4)
- [Data inspection video](https://github.com/mithi/little-miss-trendy/blob/master/A-AV1/videos/x-many-images-unified.mp4)

## Directory `./A-AV2/`
- Contains behavioral cloning work to make a car run autonomously on app `formula-trend-1.0.0-alpha.5`
- Contains behavioral cloning work to make a car run autonomously on app `formula-trend-1.0.0-beta.3`

### Videos
- [beta3 track1 red 4 laps normal](https://youtu.be/n_deohu4i0E)
- [beta3 track2 red 4 laps normal](https://youtu.be/vV3112WJ48o)
- [beta3 track3 red normal](https://youtu.be/GTjTX_WTKNc)
- [alpha5 track3 red 10 laps timelapse](https://youtu.be/5LhN1_r9p9w)
- [alpha5 track3 red 10 laps normal](https://youtu.be/DRkD2LPB3_Q)
- [alpha5 track2 green 10 laps timelapse](https://youtu.be/pIQipid5GtQ)
- [alpha5 track2 red 10 laps timelapse](https://youtu.be/t3wT8Googsc)
- [alpha5 track2 green 10 laps normal](https://youtu.be/A96RF0BXZns)
- [alpha5 track2 red 10 laps normal](https://youtu.be/5LhN1_r9p9w)

## Directory `./A-AV3/`
- Contains models and script to make a car run autonomously on the apps
```
formula-trend-1.0.0-alpha.5
formula-trend-1.0.0-beta.3
```

## TO IMPROVE THE MODEL AND PERFORMANCE
- Include more data of "recovery driving", IE during turns if it overshoots, it should have data how to
recover from the overshooting.
- Rerun with different batch size, epoch and other parameters. Play with preprocessing use different color presentation etc etc.
- Play with hyperparameters in `drive.py`
```python
# Tweak parameters to adjust the throttle
# throttle = THROTTLE_MAX - C_SPEED * (speed / MAX_SPEED)**2 - C_STEER * (steering_angle / MAX_ANGLE)**2
# throttle = max(THROTTLE_MIN, throttle)
THROTTLE_MAX = 0.79
THROTTLE_MIN = 0.01
C_SPEED = 1.0
C_STEER = 40.0


# BETA 3: RED - TRACK 1
# THROTTLE_MAX=0.6 C_STEER=50, THROTTLE_MIN=0.1, C_SPEED=1.0

# BETA 3: RED - TRACK 2, TRACK3
# THROTTLE_MAX=0.8, C_STEER=40, THROTTLE_MIN=0.1, C_SPEED=1.0
```


## [The three apps for mac can be downloaded in this Dropbox link](https://www.dropbox.com/sh/6ktu5bfuv34ua5r/AABu4xrCMuWagfJhjRExvPdza?dl=0)
