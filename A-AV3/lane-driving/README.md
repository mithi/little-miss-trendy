
# RUN
```
$ pwd
~/Desktop/DONOTBACKUP/apps/formula-trend-1.0.0-beta.3/Mac/formula-trend-1.0.0-beta.3.app/Contents/MacOS
$ ./formula-trend-1.0.0-beta.3

$ python drive.py ./models/red.h5
# or

$ python drive.py ./models/green.h5
```

# Tweak parameters in `drive.py`
```python
# Tweak parameters to adjust the throttle
# throttle = THROTTLE_MAX - C_SPEED * (speed / MAX_SPEED)**2 - C_STEER * (steering_angle / MAX_ANGLE)**2
# throttle = max(THROTTLE_MIN, throttle)
THROTTLE_MAX = 0.79
THROTTLE_MIN = 0.01
C_SPEED = 1.0
C_STEER = 40.0

# BETA 3: RED - TRACK 2, TRACK3
# THROTTLE_MAX=0.8, C_STEER=40, THROTTLE_MIN=0.1, C_SPEED=1.0

# BETA 3: RED - TRACK 1
# THROTTLE_MAX=0.6 C_STEER=50, THROTTLE_MIN=0.1, C_SPEED=1.0
```
