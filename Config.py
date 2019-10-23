import numpy as np
from math import sin, cos, pi
#import tensorflow as tf
####################################################################################
##################################### CONFIG #######################################
class Config(object):
    ###============ player params =========
    CAP_RANGE = 2.
    VD = 1.
    VI = 1.5
    TAG_RANGE = 5.
    
    TIME_STEP = 0.1
    
    ##========= target =========

    x0 = [np.array([0., 2.*CAP_RANGE+TAG_RANGE]), (1.99*CAP_RANGE+TAG_RANGE)*np.array([sin(pi/4), cos(pi/4)])]

    ###============ learning params =========
    LEARNING_RATE = 0.01
    LAYER_SIZES = [30, 6, 30]
    # ACT_FUNCS = [tf.nn.tanh, tf.nn.tanh, tf.nn.tanh]
    TAU = 0.01
    MAX_BUFFER_SIZE = 10000
    BATCH_SIZE = 1000
    TRAIN_STEPS = 100
    TARGET_UPDATE_INTERVAL = 1

    ###============ saving params =========
    DATA_FILE = 'valueData.csv'
    MODEL_DIR = 'models/'
    MODEL_FILE = 'valueFn'

    SAVE_FREQUENCY = 100
    PRINTING_FREQUENCY = 50
