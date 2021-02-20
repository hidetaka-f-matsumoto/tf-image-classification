# TF Image Classification

Skelton for image classification with TensorFlow.

## Test

```sh
$ python scripts/test.py -d dataset/test -m models/hoo -s 480 -o out/hoo/result.csv
```

## Grad CAM

```sh
$ python scripts/grad_cam.py -d dataset/test/ -m models/hoo -s 480 -l conv2d_2 -o out/hoo/grad_cam/
```

## Build report html

```sh
$ ruby scripts/build_result_html.rb out/hoo/result.csv out/hoo/grad_cam/ out/hoo/result.html
```
