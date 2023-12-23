import requests
import json
import re
from .lc_option import LcOption

# https://houbb.github.io/2019/02/25/github-09-pic-bed


TARGET_RE = r'"pics":(.*)\}\}'
PIC_HOST = 'https://tva1.sinaimg.cn/'
SIZES = 'large|bmiddle|mw1024|mw690|small|square|thumb180|thumbnail'.split('|')
API_URL = 'https://picupload.weibo.com/interface/pic_upload.php?ori=1&data={}&mime=image%2F{}'


class Weibo:

    @staticmethod
    def help():
        helpstr = """
    基本功能说明:
    1. 上传图片到 weibo，并获取地址
    2. 支持 jpg/png/gif 等常用图片格式，不过，返回地址是 jpg/gif 2种格式
    3. 只支持单张图片上传，不支持多张图片上传
    
    参考说明：
    source: 原始图片路径 或者 base64 串
    mode: 上传模式，可选值为 base64 或者 file
    format: 图片格式，可选值为 jpg/gif
    debug: 是否开启 debug 模式，可选值为 True/False
            """
        print(helpstr)

    @property
    def headers(self):
        return {'Cookie': f'SUB={self.token}', 'Referer': 'https://weibo.com/'}

    def __init__(self):
        lc_opt = LcOption()
        res = lc_opt.get('60f768f6d9f1465d3b1d5c43')
        self.token = res['value']

    # Get the image url by pid and size.
    def get(self, pid, size='large', format='jpg'):
        if size not in SIZES:
            size = 'large'
        return PIC_HOST + size + '/' + pid + '.' + format

    # Get all kinds of image url by pid.
    def getall(self, pid, format='jpg'):
        return {
            'large': self.get(pid, 'large', format),
            'bmiddle': self.get(pid, 'bmiddle', format),
            'mw1024': self.get(pid, 'mw1024', format),
            'mw690': self.get(pid, 'mw690', format),
            'small': self.get(pid, 'small', format),
            'square': self.get(pid, 'square', format),
            'thumb180': self.get(pid, 'thumb180', format),
            'thumbnail': self.get(pid, 'thumbnail', format),
        }

    # Upload image by url.
    def upload(self, **kwargs):
        source = kwargs.get('source')
        mode = kwargs.get('mode', 'file')
        fmt = kwargs.get('format', 'jpg')
        debug = kwargs.get('debug', False)
        files = {'pic1': source, }
        if mode == 'file':
            filep = open(source, 'rb')
            files = {'pic1': filep, }
        elif mode == 'base64':
            filep = source
            files = {'b64_data': filep}
        elif mode == 'url':
            res = requests.get(source, verify=False)
            filep = res.content
            files = {'pic1': filep}

        url = API_URL.format(mode, fmt)
        res = requests.post(url, files=files, headers=self.headers)
        html = res.text

        if debug:
            print(url, files, self.headers)
            print("Response HTML: ", html)

        target_str = re.findall(TARGET_RE, html)[0]
        json_data = json.loads(target_str)
        pdata = json_data['pic_1']
        pid = pdata.get('pid', None)
        is_success = bool(pid) and pdata.get('width', 0) > 0

        if is_success:
            return {
                'success': True,
                'pid': pid,
                'url': self.get(pid, 'large', fmt),
                **pdata
            }
        else:
            return {
                'success': False,
                'pid': None,
                'url': None,
                **pdata
            }
