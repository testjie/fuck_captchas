# -*- coding:utf-8 -*-
__author__ = 'snake'
import numpy as np
import tensorflow as tf
from PIL import Image
from config import CNN_WAP_PATH


def _convert2gray(img):
    if len(img.shape)>2:
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    else:
        return img





def cnn(b_alpha=0.1,X=None, keep_prob=None, IMAGE_HEIGHT=80, IMAGE_WIDTH=200, MAX_CAPTCHA=4, CHAR_SET_LEN=10):
    """
    3层卷积神经网络
    :param b_alpha:
    :return:
    """
    x = tf.reshape(X, shape=[-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])

    wc1 = tf.get_variable(name='wc1', shape=[3, 3, 1, 32],
                          dtype=tf.float32, initializer=tf.contrib.layers.xavier_initializer())
    bc1 = tf.Variable(b_alpha * tf.random_normal([32]))
    conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, wc1, strides=[1, 1, 1, 1], padding='SAME'), bc1))  # 输出大小不变
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv1 = tf.nn.dropout(conv1, keep_prob)

    wc2 = tf.get_variable(name='wc2', shape=[3, 3, 32, 64],
                          dtype=tf.float32, initializer=tf.contrib.layers.xavier_initializer())
    bc2 = tf.Variable(b_alpha * tf.random_normal([64]))
    conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, wc2, strides=[1, 1, 1, 1], padding='SAME'), bc2))
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv2 = tf.nn.dropout(conv2, keep_prob)

    wc3 = tf.get_variable(name='wc3', shape=[3, 3, 64, 128],
                          dtype=tf.float32, initializer=tf.contrib.layers.xavier_initializer())
    bc3 = tf.Variable(b_alpha * tf.random_normal([128]))
    conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, wc3, strides=[1, 1, 1, 1], padding='SAME'), bc3))
    conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv3 = tf.nn.dropout(conv3, keep_prob)

    wd1 = tf.get_variable(name='wd1', shape=[10 * 25 * 128, 1024],
                          dtype=tf.float32, initializer=tf.contrib.layers.xavier_initializer())
    bd1 = tf.Variable(b_alpha * tf.random_normal([1024]))
    dense = tf.reshape(conv3, [-1, 10 * 25 * 128])
    dense = tf.nn.relu(tf.add(tf.matmul(dense, wd1), bd1))
    dense = tf.nn.dropout(dense, keep_prob)

    wout = tf.get_variable('name', shape=[1024, MAX_CAPTCHA * CHAR_SET_LEN],
                           dtype=tf.float32, initializer=tf.contrib.layers.xavier_initializer())
    bout = tf.Variable(b_alpha * tf.random_normal([MAX_CAPTCHA * CHAR_SET_LEN]))
    out = tf.add(tf.matmul(dense, wout), bout)

    return out


def fuck_captcha(image_path=None, max_captcha=4, char_set_len=10, image_height=80, image_width=200):
    """
    破解验证码方法
    :param image_path:
    :param max_captcha:
    :param char_set_len:
    :param image_height:
    :param image_width:
    :return:
    """
    if image_path is None or image_path == "":
        return ""

    # 初始化占位符
    X = tf.placeholder(tf.float32, [None, image_height * image_width])
    keep_prob = tf.placeholder(tf.float32)

    # 建立cnn模型
    output = cnn(X=X, keep_prob=keep_prob)
    saver = tf.train.Saver()
    predict = tf.argmax(tf.reshape(output, [-1, max_captcha, char_set_len]), 2)

    with tf.Session() as sess:
        captcha_image = np.array(Image.open(image_path))
        saver.restore(sess, tf.train.latest_checkpoint(CNN_WAP_PATH))
        image = _convert2gray(captcha_image)
        image = image.flatten() / 255

        # 解析预测值
        text_list = sess.run(predict, feed_dict={X: [image], keep_prob: 1})
        text = text_list[0].tolist()
        text = "".join(list(map(str, text)))

    return text


if __name__ == "__main__":
    image_path = "../uploads/4941.jpg"
    print(fuck_captcha(image_path=image_path))