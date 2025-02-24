from keras.layers import (Activation, BatchNormalization, Conv2D, Input,
                          MaxPooling2D, UpSampling2D, concatenate)
from keras.layers import MaxPool2D, GlobalAveragePooling2D, Dense
from keras.optimizers import Adam, RMSprop                        
from keras.models import Model, Sequential
from keras.optimizers import RMSprop

from utils.params import *
from utils.losses import *

def get_manufacturer_model():

    """
        Get model to predict car manufacturer given an input image. 
    """
    manufacturer_model = Sequential()
    manufacturer_model.add(Conv2D(16, kernel_size= (3, 3), activation="relu",
                                input_shape = (INPUT_SIZE, INPUT_SIZE, 3)))
    manufacturer_model.add(MaxPool2D())
    manufacturer_model.add(Conv2D(32, kernel_size = (3, 3), activation = "relu"))
    manufacturer_model.add(MaxPool2D())
    manufacturer_model.add(Conv2D(64, kernel_size = (3, 3), activation = "relu"))
    manufacturer_model.add(MaxPool2D())
    manufacturer_model.add(Conv2D(128, kernel_size = (3, 3), activation = "relu"))
    manufacturer_model.add(MaxPool2D())
    # manufacturer_model.add(Conv2D(256, kernel_size = (3, 3), activation = "relu"))
    # manufacturer_model.add(MaxPool2D())
    # manufacturer_model.add(Conv2D(512, kernel_size = (3, 3), activation = "relu"))
    # manufacturer_model.add(MaxPool2D())
    manufacturer_model.add(GlobalAveragePooling2D())
    manufacturer_model.add(Dense(36, activation = 'softmax')) # Number of makers in the dataset

    manufacturer_model.compile(optimizer = Adam(), loss = 'categorical_crossentropy', metrics = ['accuracy'])
    return manufacturer_model

def get_baseline_model(input_shape=(128, 128, 3)):
    """
        Get a simple 3 layer CNN model to compute mask given an input image. 
    """
    
    baseline_model = Sequential()
    baseline_model.add( Conv2D(16, kernel_size= (3, 3), activation='relu', padding='same', input_shape=(INPUT_SIZE, INPUT_SIZE, 3)) )
    baseline_model.add( Conv2D(32, kernel_size= (3, 3), activation='relu', padding='same') )
    baseline_model.add( Conv2D(1, kernel_size=(5, 5), activation='sigmoid', padding='same') )    

    # baseline_model.summary()
    # SVG(model_to_dot(baseline_model).create(prog='dot', format='svg'))
    
    baseline_model.compile(Adam(lr=1e-3), bce_dice_loss, metrics=['accuracy', dice_coeff])

    return baseline_model


def get_unet_128(input_shape=(128, 128, 3),
                 num_classes=1):
    """
        Get a Unet based CNN model to compute mask given an input image if size(128X128). 
    """
    inputs = Input(shape=input_shape)
    # 128        

    down1 = Conv2D(64, (3, 3), padding='same')(inputs)
    down1 = BatchNormalization()(down1)
    down1 = Activation('relu')(down1)
    down1 = Conv2D(64, (3, 3), padding='same')(down1)
    down1 = BatchNormalization()(down1)
    down1 = Activation('relu')(down1)
    down1_pool = MaxPooling2D((2, 2), strides=(2, 2))(down1)
    # 64

    down2 = Conv2D(128, (3, 3), padding='same')(down1_pool)
    down2 = BatchNormalization()(down2)
    down2 = Activation('relu')(down2)
    down2 = Conv2D(128, (3, 3), padding='same')(down2)
    down2 = BatchNormalization()(down2)
    down2 = Activation('relu')(down2)
    down2_pool = MaxPooling2D((2, 2), strides=(2, 2))(down2)
    # 32

    down3 = Conv2D(256, (3, 3), padding='same')(down2_pool)
    down3 = BatchNormalization()(down3)
    down3 = Activation('relu')(down3)
    down3 = Conv2D(256, (3, 3), padding='same')(down3)
    down3 = BatchNormalization()(down3)
    down3 = Activation('relu')(down3)
    down3_pool = MaxPooling2D((2, 2), strides=(2, 2))(down3)
    # 16

    # down4 = Conv2D(512, (3, 3), padding='same')(down3_pool)
    # down4 = BatchNormalization()(down4)
    # down4 = Activation('relu')(down4)
    # down4 = Conv2D(512, (3, 3), padding='same')(down4)
    # down4 = BatchNormalization()(down4)
    # down4 = Activation('relu')(down4)
    # down4_pool = MaxPooling2D((2, 2), strides=(2, 2))(down4)
    # 8

    center = Conv2D(512, (3, 3), padding='same')(down3_pool)
    center = BatchNormalization()(center)
    center = Activation('relu')(center)
    center = Conv2D(512, (3, 3), padding='same')(center)
    center = BatchNormalization()(center)
    center = Activation('relu')(center)
    # center

    # up4 = UpSampling2D((2, 2))(center)
    # up4 = concatenate([down4, up4], axis=3)
    # up4 = Conv2D(512, (3, 3), padding='same')(up4)
    # up4 = BatchNormalization()(up4)
    # up4 = Activation('relu')(up4)
    # up4 = Conv2D(512, (3, 3), padding='same')(up4)
    # up4 = BatchNormalization()(up4)
    # up4 = Activation('relu')(up4)
    # up4 = Conv2D(512, (3, 3), padding='same')(up4)
    # up4 = BatchNormalization()(up4)
    # up4 = Activation('relu')(up4)
    # 16

    up3 = UpSampling2D((2, 2))(center)
    up3 = concatenate([down3, up3], axis=3)
    up3 = Conv2D(256, (3, 3), padding='same')(up3)
    up3 = BatchNormalization()(up3)
    up3 = Activation('relu')(up3)
    up3 = Conv2D(256, (3, 3), padding='same')(up3)
    up3 = BatchNormalization()(up3)
    up3 = Activation('relu')(up3)
    up3 = Conv2D(256, (3, 3), padding='same')(up3)
    up3 = BatchNormalization()(up3)
    up3 = Activation('relu')(up3)
    # 32

    up2 = UpSampling2D((2, 2))(up3)
    up2 = concatenate([down2, up2], axis=3)
    up2 = Conv2D(128, (3, 3), padding='same')(up2)
    up2 = BatchNormalization()(up2)
    up2 = Activation('relu')(up2)
    up2 = Conv2D(128, (3, 3), padding='same')(up2)
    up2 = BatchNormalization()(up2)
    up2 = Activation('relu')(up2)
    up2 = Conv2D(128, (3, 3), padding='same')(up2)
    up2 = BatchNormalization()(up2)
    up2 = Activation('relu')(up2)
    # 64

    up1 = UpSampling2D((2, 2))(up2)
    up1 = concatenate([down1, up1], axis=3)
    up1 = Conv2D(64, (3, 3), padding='same')(up1)
    up1 = BatchNormalization()(up1)
    up1 = Activation('relu')(up1)
    up1 = Conv2D(64, (3, 3), padding='same')(up1)
    up1 = BatchNormalization()(up1)
    up1 = Activation('relu')(up1)
    up1 = Conv2D(64, (3, 3), padding='same')(up1)
    up1 = BatchNormalization()(up1)
    up1 = Activation('relu')(up1)
    # 128

    classify = Conv2D(num_classes, (1, 1), activation='sigmoid')(up1)

    model = Model(inputs=inputs, outputs=classify)

    model.compile(optimizer=RMSprop(lr=0.0001), loss=bce_dice_loss, metrics=[dice_coeff])

    return model
