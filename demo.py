# -*- coding: utf-8 -*
import rsa

# 生成密钥
(pubkey, privkey) = rsa.newkeys(1024)

# # 保存密钥
# with open('rsa_key/public.pem', 'w+') as f:
#     f.write(pubkey.save_pkcs1().decode())
#
# with open('rsa_key/private.pem', 'w+') as f:
#     f.write(privkey.save_pkcs1().decode())

# 导入密钥
with open('rsa_key/public.pem', 'r') as f:
    pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

with open('rsa_key/private.pem', 'r') as f:
    privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())


caffe_path = "/home/aiserver/code/dl_pipline_v0/model/ssd/deploy.prototxt"
prototxt_path = "/home/aiserver/code/dl_pipline_v0/model/ssd/ResNetBody_rev1_pipline_data_v1_256x256_iter_74512.caffemodel"

encoder_caffemodel = "rsa_key/rsa_key.model"
encoder_prototxt = "rsa_key/rsa_key.parameter"

decoder_caffemodel = "rsa_key/ssd.caffemodel"
decoder_prototxt = "rsa_key/ssd.prototxt"


def rsa_encoder(in_path, out_path):
    ff = open(in_path, "rb")

    f_model = open(out_path, "wb")

    while True:
        content = ff.read(100)
        if not content:
            break
        print(content)
        ##读取caffemodel
        # 明文
        message = content
        # 公钥加密
        crypto = rsa.encrypt(message, pubkey)

        # 私钥解密
        message = rsa.decrypt(crypto, privkey)
        print(crypto.__len__())
        print(message.__len__())
        f_model.write(crypto)

        # # 私钥签名
        # signature = rsa.sign(message, privkey, 'SHA-1')
        #
        # # 公钥验证
        # rsa.verify(message, signature, pubkey)

    f_model.close()
    ff.close()

def rsa_decoder(in_path, out_path):
    ff = open(in_path, "rb")
    f_caffe = open(out_path,"wb")
    while True:
        content = ff.read(128)
        if not content:
            break
        #print(content)
        ##读取caffemodel
        # 私钥解密
        message = rsa.decrypt(content, privkey)
        print(content.__len__())
        print(message)
        f_caffe.write(message)

    ff.close()
    f_caffe.close()

rsa_encoder(caffe_path, encoder_caffemodel)
rsa_decoder(encoder_caffemodel, decoder_caffemodel)

rsa_encoder(prototxt_path, encoder_prototxt)
rsa_decoder(encoder_prototxt, decoder_prototxt)
