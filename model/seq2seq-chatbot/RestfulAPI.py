# encoding: utf-8

import os

import tensorflow as tf
import numpy as np

from SequenceToSequence import Seq2Seq
import DataProcessing
from CONFIG import BASE_MODEL_DIR, MODEL_NAME, data_config, model_config

import tornado.web
import tornado.ioloop
from tornado.web import RequestHandler


def chatbot_api(infos):
    du = DataProcessing.DataUnit(**data_config)
    save_path = os.path.join(BASE_MODEL_DIR, MODEL_NAME)
    batch_size = 1
    tf.reset_default_graph()
    model = Seq2Seq(batch_size=batch_size,
                    encoder_vocab_size=du.vocab_size,
                    decoder_vocab_size=du.vocab_size,
                    mode='decode',
                    **model_config)
    # 创建session的时候允许显存增长
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    with tf.Session(config=config) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        model.load(sess, save_path)
        while True:
            q = infos
            if q is None or q.strip() == '':
                return "请输入聊天信息"
                continue
            q = q.strip()
            indexs = du.transform_sentence(q) # 把句子转换为索引
            x = np.asarray(indexs).reshape((1, -1))  # 转为1行
            xl = np.asarray(len(indexs)).reshape((1,))
            pred = model.predict(
                sess, np.array(x),
                np.array(xl)
            )
            result = du.transform_indexs(pred[0])  # 将索引转为句子
            return result


class BaseHandler(RequestHandler):
    """解决JS跨域请求问题"""

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        # self.set_header('Content-type', 'application/json')


class IndexHandler(BaseHandler):
    # 添加一个处理get请求方式的方法
    def get(self):
        # 向响应中，添加数据
        infos = self.get_query_argument("infos")
        print("Q:", infos)
        # 捕捉服务器异常信息
        try:
            result = chatbot_api(infos=infos)
        except:
            result = "这个问题我暂时不会,换个问题吧"
        if result == '':
            result = "这个问题我暂时不会,换个问题吧"
        print("A:", "".join(result))
        self.write("".join(result))
    
    def options(self):
        print(self)
        infos = self.get_query_argument("infos")
        print("Q:", infos)
        # 捕捉服务器异常信息
        try:
            result = chatbot_api(infos=infos)
        except:
            result = "这个问题我暂时不会,换个问题吧"
        if result == '':
            result = "这个问题我暂时不会,换个问题吧"
        print("A:", "".join(result))
        self.write("".join(result))



if __name__ == '__main__':
    # 创建一个应用对象
    app = tornado.web.Application([(r'/api/chatbot', IndexHandler)])
    # 绑定一个监听端口
    app.listen(8888)
    # 启动web程序，开始监听端口的连接
    tornado.ioloop.IOLoop.current().start()
