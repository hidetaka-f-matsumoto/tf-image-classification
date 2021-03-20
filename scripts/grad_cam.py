import os
import glob
import argparse
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img

os.environ['KMP_DUPLICATE_LIB_OK']='True'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', help='dataset directory')
    parser.add_argument('-i', '--image', help='image path')
    parser.add_argument('-s', '--size', required=True, type=int, default=480, help='width and height of image')
    parser.add_argument('-m', '--model', required=True, help='model path to load')
    parser.add_argument('-l', '--layer', required=True, help='layer to explain')
    parser.add_argument('-sh', '--show', action='store_true', help='show image if specified')
    parser.add_argument('-o', '--output', help='output image path')
    args = parser.parse_args()
    if not args.dataset and not args.image:
        parser.error('-d or -i is required.')
    return args


def grad_cam(input_model, x, size, layer_name):
    """
    Args:
        input_model(object): モデルオブジェクト
        x(ndarray): 画像
        size(width, height): 画像サイズ
        layer_name(string): 畳み込み層の名前
    Returns:
        output_image(ndarray): 元の画像に色付けした画像
    """

    # 画像の前処理
    # 読み込む画像が1枚なため、次元を増やしておかないとmode.predictが出来ない
    X = np.expand_dims(x, axis=0)
    preprocessed_input = X.astype('float32') / 255.0

    grad_model = models.Model([input_model.inputs], [input_model.get_layer(layer_name).output, input_model.output])

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(preprocessed_input)
        class_idx = np.argmax(predictions[0])
        loss = predictions[:, class_idx]

    # 勾配を計算
    output = conv_outputs[0]
    grads = tape.gradient(loss, conv_outputs)[0]

    gate_f = tf.cast(output > 0, 'float32')
    gate_r = tf.cast(grads > 0, 'float32')

    guided_grads = gate_f * gate_r * grads

    # 重みを平均化して、レイヤーの出力に乗じる
    weights = np.mean(guided_grads, axis=(0, 1))
    cam = np.dot(output, weights)

    # 画像を元画像と同じ大きさにスケーリング
    cam = cv2.resize(cam, size, cv2.INTER_LINEAR)
    # ReLUの代わり
    cam  = np.maximum(cam, 0)
    # ヒートマップを計算
    heatmap = cam / cam.max()

    # モノクロ画像に疑似的に色をつける
    jet_cam = cv2.applyColorMap(np.uint8(255.0*heatmap), cv2.COLORMAP_JET)
    # RGBに変換
    rgb_cam = cv2.cvtColor(jet_cam, cv2.COLOR_BGR2RGB)
    # もとの画像に合成
    output_image = (np.float32(rgb_cam) + x / 2)

    return output_image

def exec(model, path, size, layer, show=False, output=None):
    src = img_to_array(load_img(path, target_size=size))
    if show:
        src_img = array_to_img(src)
        src_img.show()

    cam = grad_cam(model, src, size, layer)
    cam_img = array_to_img(cam)
    if show:
        cam_img.show()
    if output:
        cam_img.save(output)

if __name__ == "__main__":
    args = parse_args()
    model = models.load_model(args.model)

    if args.dataset:
        for path in glob.iglob('{dir}/**/*.jpeg'.format(dir=args.dataset)):
            filename = os.path.basename(path)
            out_path = '{dir}/{filename}'.format(dir=args.output, filename=filename)
            print(out_path)
            exec(model, path, (args.size, args.size), args.layer,
                show=args.show, output=out_path)
    elif args.image:
        exec(model, args.image, (args.size, args.size), args.layer,
            show=args.show, output=args.output)
