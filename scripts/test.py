import os
import glob
import argparse
from skimage import io
import numpy as np
from skimage.transform import resize
import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

# %matplotlib inline

os.environ['KMP_DUPLICATE_LIB_OK']='True'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', required=True, help='dataset directory')
    parser.add_argument('-m', '--model', required=True, help='model path to load')
    parser.add_argument('-s', '--size', required=True, type=int, default=480, help='width and height of image')
    parser.add_argument('-o', '--output', required=True, help='output file path')
    return parser.parse_args()

def test_total(dataset_dir, input_width, input_height, model):
    test_datagen = ImageDataGenerator(rescale=1./255)
    batch_size = 10
    test_generator = test_datagen.flow_from_directory(
        dataset_dir,
        target_size=(input_width,input_height),
        batch_size=batch_size,
        class_mode='binary')
    test_loss, test_acc = model.evaluate_generator(test_generator, steps=test_generator.samples // batch_size)
    return test_loss, test_acc

def test_each(dataset_dir, input_width, input_height, model):
    result = []
    for path in glob.glob('{}/**/*.jpeg'.format(dataset_dir)):
        x = img_to_array(load_img(path, target_size=(input_width, input_height)))
        score = model.predict(np.expand_dims(x[:,:,0:3]/255, axis=0), verbose=1)
        result.append([path, score[0][0]])

    return np.array(result)


if __name__ == "__main__":
    args = parse_args()
    model = models.load_model(args.model)
    test_loss, test_acc = test_total(args.dataset, args.size, args.size, model)
    print('test loss: {}, accuracy: {}'.format(test_loss, test_acc))
    result = test_each(args.dataset, args.size, args.size, model)
    if args.output:
        np.savetxt(args.output, result, delimiter=',', fmt='%s')
    else:
        print(result)
