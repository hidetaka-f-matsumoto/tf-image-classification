import os
import argparse
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import optimizers
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import CSVLogger

os.environ['KMP_DUPLICATE_LIB_OK']='True'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', required=True, help='dataset directory')
    parser.add_argument('-m', '--model', required=True, help='model path to save')
    parser.add_argument('-s', '--size', required=True, type=int, default=480, help='width and height of image')
    return parser.parse_args()

def train(dataset_dir, input_width, input_height):
    model = models.Sequential()

    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=(input_width, input_height, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(GlobalAveragePooling2D())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=1e-4),
                metrics=['acc'])

    model.summary()

    train_dir = './{dataset_dir}/train'.format(dataset_dir=dataset_dir)
    validation_dir = './{dataset_dir}/validation'.format(dataset_dir=dataset_dir)

    # 回転や拡大縮小によりデータ数を水増し
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,)

    test_datagen = ImageDataGenerator(rescale=1./255)

    # 学習用データ読込み
    train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(input_width, input_height),
            batch_size=30,
            class_mode='binary')

    # 訓練時検証用データ読込み
    validation_generator = test_datagen.flow_from_directory(
            validation_dir,
            target_size=(input_width, input_height),
            batch_size=30,
            class_mode='binary')

    history = model.fit_generator(
        train_generator,
        steps_per_epoch=100,
        epochs=10,
        validation_data=validation_generator,
        validation_steps=10,
        callbacks=[CSVLogger('training.log')])

    return model, history

if __name__ == "__main__":
    args = parse_args()
    model, history = train(args.dataset, args.size, args.size)
    if args.model:
        # 処理時間が長いため途中から再開できるようできた学習モデルを保存しておく
        model.save(args.model)
        hist_df = pd.DataFrame(history.history)
        hist_df.to_csv('{model_dir}/train_history.csv'.format(model_dir=args.model))
