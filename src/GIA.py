import json
import tkinter
import warnings
import win32api
import win32con
import win32gui
import logging
from time import sleep
from io import BytesIO
from typing import Tuple
from sys import exit, argv
from json import load, dump
from PIL import Image, ImageTk
from threading import Thread
from datetime import datetime
from requests import get, post
from random import sample, randint
from urllib.request import urlopen
from tkinter.colorchooser import askcolor
from requests.exceptions import ConnectionError
from os import listdir, remove, mkdir, startfile
from tkinter.messagebox import showinfo, askyesno
from os.path import dirname, join, basename, exists, abspath
from tkinter.filedialog import asksaveasfilename, askopenfilename, askdirectory

exec('import requests')
exec('requests.packages.urllib3.disable_warnings()')
warnings.filterwarnings("ignore")

main_path = '/'.join(argv[0].split("\\")[:-2])

bing_config = {
    "urls": ["https://api.yimian.xyz/img"],
    "request_params": {"https://api.yimian.xyz/img": {"type": "wallpaper"}},
    "request_datas": {},
    "response_processing": {},
    "proxies": {},
    "support_type": [
        "BMP", "CUR", "DCX", "FLI", "FLC ", "FPX", "GBR", "GD", "GIF", "ICO", "IM", "IMT", "JPEG", "JPG", "MCIDAS",
        "MIC", "MSP",
        "PCD", "PCX", "PIXAR", "PNG", "PPM", "PSD", "SGI", "SPIDER", "TGA ", "TIFF", "WAL", "WMF", "XBM", "XPM"]
}

setu_r18_config = {
    "urls": ["https://moe.jitsu.top/img/"],
    "request_params": {"https://moe.jitsu.top/img/": {"sort": "r18"}},
    "request_datas": {},
    "response_processing": {},
    "proxies": {},
    "support_type": [
        "BMP", "CUR", "DCX", "FLI", "FLC ", "FPX", "GBR", "GD", "GIF", "ICO", "IM", "IMT", "JPEG", "JPG", "MCIDAS",
        "MIC", "MSP",
        "PCD", "PCX", "PIXAR", "PNG", "PPM", "PSD", "SGI", "SPIDER", "TGA ", "TIFF", "WAL", "WMF", "XBM", "XPM"]
}

init_ua = {
    "chrome": [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 "
        "Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 "
        "Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 "
        "Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 "
        "Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 "
        "Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 "
        "Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 "
        "Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 "
        "Safari/537.36 "
    ],
    "opera": [
        "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2",
        "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.14.1) Presto/2.12.388 Version/12.16",
        "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
        "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14"
    ],
    "firefox": [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0"]
}

init_set = {
    "img_load_mode": Image.NEAREST,
    "img_load_mode_info": "????????????",
    "now_url_index": 0,
    "switch": "order",
    "acquired_mode": "web",
    "switch_interval": 30,
    "retry_count_max": 5,
    "history_count_max": 50,
    "auto_save_dir": f'{main_path}/Data/img/save',
    "auto_save_do": False,
    "wallpaper_bg_color": (0, 0, 0),
    "ask_color_all": ((0, 0, 0), '#000000'),
    "full_screen_mode": True,
    "switch_wallpaper": False,
    "default_external_viewer": False,
    "now_file_dir": '/',
    "now_file_dir_list": [],
    "now_file_dir_list_len": 0,
    "now_file_path": f'{main_path}/Data/img/temp/temp.png',
    "now_config_file_path": f'{main_path}/Data/config/config.json',
    "run_log": False
}

# init_config = setu_r18_config
init_config = bing_config


class GetImgAPI:
    def __init__(self, master: tkinter.Tk = None):
        self.create_work_dirs()
        self.show_w_h = None
        if type(master) != tkinter.Tk:
            root = tkinter.Tk()
            root.title('GIA')
            root.geometry('{}x{}'.format(*root.maxsize()))
            self.master = root
            if not exists(f'{main_path}/Data/img/icon/icon.ico'):
                with open(file=f'{main_path}/Data/img/icon/icon.ico', mode='wb'
                          ) as save_icon_file, urlopen(
                    url='https://icon-icons.com/downloadimage.php?id=213814&root'
                        '=3392/ICO/64/&file=python_icon_213814.ico') as get_icon_file:
                    save_icon_file.write(get_icon_file.read())
            self.master.iconbitmap(f'{main_path}/Data/img/icon/icon.ico')
        else:
            self.master = master
        showinfo(title='??????',
                 message='\t??????????????????\n\t??????????????????\n\t??????????????????'
                         '\n\t??????Esc???????????????\n~????????????????????????,???????????????~')

        # settings.json
        self.settings_names = [
            'img_load_mode', 'img_load_mode_info', 'now_url_index',
            'switch', 'acquired_mode', 'switch_interval',
            'retry_count_max', 'history_count_max', 'auto_save_dir',
            'auto_save_do', 'wallpaper_bg_color', 'ask_color_all',
            'full_screen_mode', 'switch_wallpaper', 'default_external_viewer',
            'now_file_dir', 'now_file_dir_list', 'now_file_dir_list_len',
            'now_file_path', 'now_config_file_path', 'run_log']

        # wallpaper
        self.wallpaper_bg_color = (0, 0, 0)  # ??????
        self.ask_color_all = ((0, 0, 0), '#000000')  # ??????
        self.full_screen_mode = True
        self.switch_wallpaper = False

        # default_external_viewer
        self.default_external_viewer = False

        # local mode
        self.now_file_dir = '/'
        self.now_file_dir_list = []
        self.now_file_dir_list_len: int = int()
        self.now_file_path = f'{main_path}/Data/img/temp/temp.png'
        self.now_config_file_path = f'{main_path}/Data/config/config.json'
        self.temp_file_path = f'{main_path}/Data/img/temp/temp.png'

        # wed mode
        # bing_img_url = 'https://bing.biturl.top'
        # self.url = 'http://127.0.0.1:5050/Img_Test'
        self.now_img_url = ''
        #   config.json
        self.request_params: dict = {}
        self.request_params_dict: dict = {}
        self.request_data: dict = {}
        self.response_processing: str = ''
        self.url: str = ''
        self.urls_len: int = 0
        self.proxies: dict = {}
        self.proxies_dict: dict = {}
        self.response_processing_dict: dict = {}
        self.support_type: list = []
        self.request_datas: dict = {}
        self.urls: list = []
        self.UA = {}

        # history
        self.history_count_num = len(listdir(f'{main_path}/Data/img/history'))
        self.history_save_dir = f'{main_path}/Data/img/history'

        # set_up
        self.have_set_up_win = False

        # img
        self.img_load_mode = Image.NEAREST
        self.img_load_mode_info = '????????????'
        self.img_width, self.img_height = None, None
        self.the_img: Image.Image = Image.Image()
        self.the_img_tk = None
        self.original_img: Image.Image = Image.Image()
        self.now_url_index: int = 0
        self.switch = 'order'
        self.acquired_mode = 'web'
        self.switch_interval = 30
        self.retry_count_max = 5
        self.history_count_max = 50

        # auto save
        # self.auto_save_dir = f'{main_path}/Data/img/save'
        self.auto_save_dir = None
        self.auto_save_do = False
        self.file_suffix = ''
        self.auto_switch_running = False

        # screen info
        self.screen_size = (self.master.winfo_screenwidth(),
                            self.master.winfo_screenheight())

        # ??????log
        self.print_log = None
        self.run_log = False  # in settings.json
        self.init_log()

        # ????????????
        self.data_refresh()

        # info
        self.log_out(' | ?????????????????? :', self.screen_size)
        self.log_out(' | ???????????????????????? :', self.temp_file_path)

        # ??????
        self.the_img_weg = tkinter.Label(master=self.master)

        # ????????????
        self.configure_image()

        # after
        self.the_img_weg.after(
            ms=self.switch_interval * 1000, func=self.auto_switch)
        self.auto_switch_running = True

        # bind
        self.the_img_weg.bind('<Button-1>', lambda _: self.configure_image())
        self.the_img_weg.bind(
            '<Button-2>', lambda _: self.set_up() if not self.have_set_up_win else None)
        self.the_img_weg.bind('<Button-3>', lambda _: self.save_img())
        self.master.bind('<Escape>', lambda _: self.escape())

        self.master.protocol('WM_DELETE_WINDOW', lambda: self.program_close())

    @staticmethod
    def create_work_dirs():
        def _if_not_exists_mkdir(dir_path):
            if not exists(dir_path):
                mkdir(dir_path)

        # Data/img/log
        _if_not_exists_mkdir(f'{main_path}/log')
        # Data
        _if_not_exists_mkdir(f'{main_path}/Data')
        # Data/config
        _if_not_exists_mkdir(f'{main_path}/Data/config')
        # Data/img
        _if_not_exists_mkdir(f'{main_path}/Data/img')
        # Data/img/icon
        _if_not_exists_mkdir(f'{main_path}/Data/img/icon')
        # Data/img/save
        _if_not_exists_mkdir(f'{main_path}/Data/img/save')
        # Data/img/temp
        _if_not_exists_mkdir(f'{main_path}/Data/img/temp')
        # Data/img/temp/response
        _if_not_exists_mkdir(f'{main_path}/Data/img/temp/response')
        # Data/img/Wallpaper
        _if_not_exists_mkdir(f'{main_path}/Data/img/Wallpaper')
        # Data/img/history
        _if_not_exists_mkdir(f'{main_path}/Data/img/history')

        def _if_not_exists_json_file_mk(json_path, init_json_data):
            if not exists(json_path):
                with open(file=json_path, mode='w', encoding='UTF-8',
                          newline='\n') as config_file:
                    dump(fp=config_file, obj=init_json_data, indent=4, ensure_ascii=False)

        # Data/config/config.json
        _if_not_exists_json_file_mk(f'{main_path}/Data/config/config.json', init_config)
        # Data/config/UA.json
        _if_not_exists_json_file_mk(f'{main_path}/Data/config/UA.json', init_ua)
        # Data/config/settings.json
        _if_not_exists_json_file_mk(f'{main_path}/Data/config/settings.json', init_set)
        # Data/config/setu-r18.json
        _if_not_exists_json_file_mk(f'{main_path}/Data/config/setu-r18.json', setu_r18_config)

    def init_log(self):
        print('<!> ?????????????????????')
        log_file_dir = f'{main_path}/log/'
        now_log_file_name = '{}.log'.format(datetime.now().strftime('%Y-%m-%d'))
        now_log_file_path = join(log_file_dir, now_log_file_name)
        log_file_list = listdir(log_file_dir)
        for log_file_name in log_file_list:
            if log_file_name != now_log_file_name:
                remove(join(log_file_dir, log_file_name))
        log_format = '%(asctime)s %(filename)s %(levelname)s %(message)s'
        logging.basicConfig(filename=now_log_file_path, encoding='UTF-8',
                            level=logging.INFO, format=log_format, )
        logging.Logger(name='PRINT', level=logging.INFO)
        self.print_log = logging.getLogger('PRINT')
        self.print_log.info(msg='<!> This Logging Running Info!')

    def log_out(self, *args, sep=' ', level='INFO'):
        if self.run_log:
            str_list_args = [str(v) for v in args]
            msg = sep.join(str_list_args)
            if level == 'INFO':
                self.print_log.info(msg=msg)
            elif level == 'WARNING':
                self.print_log.warning(msg=msg)
            elif level == 'ERROR':
                self.print_log.error(msg=msg)
        print(*args, sep=sep)

    @staticmethod
    def is_int(var):
        try:
            if int(var) >= 0:
                return True
            else:
                return False
        except ValueError:
            return False

    @property
    def random_ua(self):
        llq = sample([_llq for _llq in self.UA], 1)[0]
        ua: str = sample(self.UA[llq], 1)[0]
        return ua

    @property
    def now_time_file_base_name(self):
        return datetime.now().strftime('%Y-%m-%d$%H_%M_%S.%f')

    def auto_switch(self):
        if self.switch_interval != 'STOP':
            self.auto_switch_running = True
            self.configure_image()
            self.master.after(ms=self.switch_interval * 1000, func=self.auto_switch)
        else:
            self.auto_switch_running = False

    def run(self):
        self.master.update()
        self.master.mainloop()

    def program_close(self):
        if askyesno(title='GIA', message='???????????????????'):
            self.save_settings()
            self.log_out('<!> ???????????? ??????????????????~', level='WARNING')
            self.master.quit()
            self.master.destroy()
            exit(0)

    def escape(self):
        self.full_screen_mode = not self.full_screen_mode
        if self.full_screen_mode:
            self.log_out('<!> ??????????????????', level='WARNING')
        else:
            self.log_out('<!> ??????????????????', level='WARNING')
        self.master.attributes('-fullscreen', self.full_screen_mode)

    def wallpaper(self):
        new_image = Image.new('RGB', self.screen_size,
                              self.wallpaper_bg_color if type(self.wallpaper_bg_color) == tuple else tuple(
                                  self.wallpaper_bg_color))  # ??????????????????
        # // ???????????????????????????????????????
        new_image.paste(self.the_img, self.show_w_h)  # ?????????????????????????????????????????????????????????
        bmp_file_path = abspath(f'{main_path}/Data/img/Wallpaper/Wallpaper.BMP')
        new_image.save(bmp_file_path)
        key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                    "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
        # 2 ??????????????????,0 ????????????
        win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(
            win32con.SPI_SETDESKWALLPAPER, bmp_file_path, 1 + 2)
        self.log_out(' | ?????????????????? :', bmp_file_path)

    def data_refresh(self):
        self.log_out('<!> ????????????????????????', level='WARNING')
        # ????????????????????????
        self.settings_refresh()
        # ?????????API????????????
        self.config_refresh()

    def config_refresh(self):
        with open(file=self.now_config_file_path, encoding='UTF-8') as jf:
            ljf = load(jf)
            self.urls: list = ljf['urls']
            self.request_datas: dict = ljf['request_datas']
            self.support_type: list = ljf["support_type"]
            self.response_processing_dict: dict = ljf["response_processing"]
            self.proxies_dict: dict = ljf["proxies"]
            self.request_params_dict: dict = ljf['request_params']
            # print(['support_type :', self.support_type])
        self.urls_len = len(self.urls)
        self.url = self.urls[0]
        if self.url in self.response_processing_dict:
            self.response_processing = self.response_processing_dict[self.url]
        else:
            self.response_processing = None
        if self.url in self.request_datas:
            self.request_data: dict = self.request_datas[self.url]
        else:
            self.request_data = None
        if self.url in self.request_params_dict:
            self.request_params: dict = self.request_params_dict[self.url]
        else:
            self.request_params = None
        if self.url in self.proxies_dict:
            self.proxies: dict = self.proxies_dict[self.url]
        else:
            self.proxies = None

        with open(f'{main_path}/Data/config/UA.json') as jf:
            ua_jf = load(fp=jf)
            self.UA = ua_jf

    def settings_refresh(self):
        with open(file=f'{main_path}/Data/config/settings.json', mode='r', encoding='UTF-8') as set_jf:
            settings = load(fp=set_jf)
            for name in self.settings_names:
                exec(f'self.{name} = settings["{name}"]')

    def save_settings(self):
        self.log_out('<!> ?????????????????????...', level='WARNING')
        with open(file=f'{main_path}/Data/config/settings.json', mode='w', encoding='UTF-8', newline='\n') as set_jf:
            settings = {}
            settings_code = '{'
            for name in self.settings_names:
                settings_code += f'"{name}" : self.{name},'
            settings_code += '}'
            settings = eval(settings_code)
            dump(fp=set_jf, obj=settings, ensure_ascii=False, indent=4)
        self.log_out('<!> ????????????????????????!', level='WARNING')

    @staticmethod
    def get_screen_size():
        tk = tkinter.Tk()
        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()
        tk.quit()
        tk.destroy()
        return width, height

    def get_image(self, url_: str = None, path: str = None, request_data_: dict = None,
                  response_processing: str = None, request_params: dict = None):
        headers = {
            'User-Agent': self.random_ua
        }

        img_f, image = None, None
        # ??????????????????
        if url_ is not None:
            # TODO: ?????????????????????
            response = None
            # ???????????????????????????
            if request_data_ is not None:
                # TODO: POST????????????
                ok = False
                retry_count = 0
                while not ok:
                    # ??????????????????????????????????????????????????????
                    if retry_count <= self.retry_count_max:
                        self.log_out('<!> API ?????????...', level='WARNING')
                        try:
                            response = post(url=url_, data=request_data_, proxies=self.proxies, headers=headers,
                                            verify=False, params=request_params)
                            self.log_out('<!> API ????????????!', level='WARNING')
                        except ConnectionError:
                            self.log_out('<!> ???????????? ??????5?????????', level='ERROR')
                            sleep(5)
                            ok = False
                        else:
                            ok = response.ok
                        retry_count += 1
                    else:
                        self.log_out('<!> ????????????????????????????????????????????????', level='WARNING')
                        return None
            # ????????????????????????
            else:
                # TODO: GET????????????
                ok = False
                retry_count = 0
                while not ok:
                    if retry_count <= self.retry_count_max:
                        try:
                            self.log_out('<!> API ?????????...', level='WARNING')
                            response = get(url=url_, proxies=self.proxies, headers=headers, verify=False,
                                           params=request_params)
                            self.log_out('<!> API ????????????!', level='WARNING')
                        except ConnectionError:
                            self.log_out('<!> ???????????? ??????5?????????', level='ERROR')
                            sleep(5)
                            ok = False
                        else:
                            ok = response.ok
                        retry_count += 1
                    else:
                        self.log_out('<!> ????????????????????????????????????????????????', level='WARNING')
                        return None
            self.log_out(' | ???????????????????????? :', response.headers['content-type'])
            # ???????????????????????????JSON
            if response.headers['content-type'] == 'application/json; charset=utf-8':
                # TODO: ??????JSON, ??????????????????????????????????????????, ????????????
                if response_processing:
                    self.log_out(' | ???????????????????????? :', response_processing)
                    exec('response_json = response.json()')
                    img_url = eval(response_processing)
                    self.log_out(' | ?????????????????? :', img_url)
                    self.log_out('<!> ?????????????????????...', level='WARNING')
                    response = get(
                        url=img_url, proxies=self.proxies, headers=headers)
                    self.log_out('<!> ????????????????????????', level='WARNING')
                    img_f = BytesIO(response.content)
                    self.now_img_url = response.url
                else:
                    raise '??????API?????????????????????JSON, ???????????????API???????????????'
            # ??????????????????????????????JSON
            else:
                # TODO: ??????????????????
                img_f = BytesIO(response.content)
                self.now_img_url = response.url

            # ????????????????????????????????????????????????
            content_type_s = response.headers['content-type']
            self.log_out(' | ?????????????????? :', content_type_s)
            old_content_file_path = '{}/Data/img/temp/response/response_content.{}'.format(
                main_path, self.file_suffix)
            if exists(old_content_file_path):
                remove(path=old_content_file_path)
            content_type_s_list = content_type_s.split('/')
            self.file_suffix = content_type_s_list[-1]
            if ';' in self.file_suffix:
                self.file_suffix = self.file_suffix.split(';')[0]
            new_content_file_path = abspath(
                '{}/Data/img/temp/response/response_content.{}'.format(main_path, self.file_suffix))
            if self.file_suffix.upper() not in self.support_type:
                self.log_out('<!> ?????????????????? {} ???????????????'.format(self.file_suffix), level='ERROR')
                return None
            with open(new_content_file_path, 'wb') as bf:
                bf.write(response.content)
                self.log_out(' | ?????????????????????????????? :', new_content_file_path)
            # ??????????????????
            self.original_img = Image.open(fp=img_f)

        # ????????????????????????
        elif path is not None:
            # TODO: ???????????????????????????
            img_f = open(path, 'rb')
            # ??????????????????
            self.original_img = Image.open(fp=img_f)
        # ??????????????????????????????????????????
        else:
            self.log_out('<!> ???????????????????????????????????????!', level='ERROR')
            raise '<!> ???????????????????????????????????????!'

        def convert_h_w(h=None, w=None):
            if h is not None:
                base_height_ = self.screen_size[1] - 10
                h_percent_ = base_height_ / float(image_size[1])
                w_size_ = int(float(image_size[0]) * float(h_percent_))
                h_size_ = base_height_
                return w_size_, h_size_
            if w is not None:
                base_width_ = self.screen_size[0] - 10
                w_percent_ = base_width_ / float(image_size[0])
                h_size_ = int(float(image_size[1]) * float(w_percent_))
                w_size_ = base_width_
                return w_size_, h_size_

        image_size = self.original_img.size
        w_size, h_size = convert_h_w(w=image_size[0])
        if h_size > self.screen_size[1]:
            w_size, h_size = convert_h_w(h=image_size[1])
        self.img_width, self.img_height = w_size, h_size

        # ??????????????????
        # ??????????????????PIL??????Image.NEAREST??????????????????????????????????????????????????????????????????????????????
        # image = image.resize((w_size, h_size), Image.ANTIALIAS)
        image = self.original_img.resize(
            (w_size, h_size), resample=self.img_load_mode)
        self.log_out(' | ???????????????????????? : ', self.img_load_mode_info)
        self.log_out(' | ?????????????????? : ', image_size)
        self.log_out(' | ?????????????????? : ', image.size)
        img_f.close()
        return image

    def center_show(self):
        show_x = self.screen_size[0] // 2 - self.img_width // 2
        show_y = self.screen_size[1] // 2 - self.img_height // 2
        self.show_w_h = show_x, show_y
        # self.the_img_weg.pack_forget()
        self.the_img_weg.place(x=show_x, y=show_y)
        self.master.update()

    def configure_image(self):
        def __configure_image():
            self.log_out('<!> ????????????', level='WARNING')
            self.get_save_img(url_=self.url, save_path=self.temp_file_path, request_data_=self.request_data,
                              response_processing=self.response_processing, request_params=self.request_params)
            if self.the_img is not None:
                self.the_img_tk = ImageTk.PhotoImage(image=self.the_img)
                self.the_img_weg.config(image=self.the_img_tk)
                self.center_show()
                self.history_in()
                if self.default_external_viewer:
                    self.the_img.show()
                if self.switch_wallpaper:
                    self.wallpaper()
                if self.auto_save_do:
                    self.auto_save()
            self.switch_url()

        Thread(target=__configure_image).start()

    def get_save_img(self, url_: str = None, request_data_: dict = None,
                     save_path: str = f'{main_path}/data/img/temp/temp.png',
                     response_processing: str = None, request_params: dict = None):
        if self.acquired_mode == 'web':
            the_img = self.get_image(url_=url_, request_data_=request_data_,
                                     response_processing=response_processing, request_params=request_params)
            if the_img is not None:
                self.the_img = the_img
        elif self.acquired_mode == 'local':
            if exists(self.now_file_path):
                self.the_img = self.get_image(path=self.now_file_path)
            else:
                self.log_out('<!> ??????????????????, ?????????????????????', level='ERROR')
                ask_img_file_path = askopenfilename(title='?????????????????????')
                if exists(ask_img_file_path):
                    self.now_file_path = ask_img_file_path
                    self.now_file_dir = dirname(self.now_file_path)
                    now_file_dir_list = listdir(self.now_file_dir)
                    for file_name in now_file_dir_list:
                        file_name_suffix = file_name.split('.')[-1].upper()
                        if file_name_suffix in self.support_type:
                            self.now_file_dir_list.append(file_name)
                    self.now_file_dir_list_len = len(self.now_file_dir_list)
                    self.the_img = self.get_image(path=self.now_file_path)
                else:
                    if ask_img_file_path == '':
                        self.log_out('<!> ?????????????????????, ?????????????????????!', level='WARNING')
                    else:
                        self.log_out('<!> ????????????????????????, ?????????????????????!', level='ERROR')
                    self.acquired_mode = 'web'

        if self.the_img:
            self.the_img.save(fp=save_path, format='PNG')

    def save_img(self):
        init_file_name = self.now_time_file_base_name + '.png'
        save_file_path = asksaveasfilename(filetypes=[('PNG', '*.png'), ('JPG', '*.jpg'), ('??????????????????', '')],
                                           defaultextension='*.png',
                                           initialdir=f'{main_path}/Data/img/save',
                                           initialfile=init_file_name)
        if save_file_path:
            self.original_img.save(fp=save_file_path)
            self.log_out('<!> ??????????????? :', save_file_path, level='WARNING')

    def history_in(self):
        # ??????????????????
        def __del_extra_history():
            while self.history_count_num > self.history_count_max:
                extra_img_path = join(self.history_save_dir,
                                      listdir(self.history_save_dir)[0])
                remove(extra_img_path)
                self.history_count_num -= 1
                self.log_out(' | ??????????????????????????? :', extra_img_path, level='WARNING')

        Thread(target=__del_extra_history).start()

        # ??????????????????
        if self.history_count_max != 0:
            file_name = self.now_time_file_base_name + '.png'
            file_path = join(self.history_save_dir, file_name)

            self.the_img.save(fp=file_path, format='PNG')
            self.log_out(' | ?????????????????? : {}'.format(file_path))
            self.history_count_num += 1

    def auto_save(self):
        file_name = self.now_time_file_base_name + '.jpg'
        file_path = join(self.auto_save_dir, file_name)
        self.original_img.save(fp=file_path, format='JPEG')
        self.log_out('<!> ??????????????????????????? :', file_path, level='WARNING')

    def set_up(self):
        self.have_set_up_win = True
        post_win = tkinter.Tk()
        post_win.title('??????')
        post_win.geometry('350x450')
        post_win.attributes("-topmost", True)
        post_win.resizable(False, False)
        post_win.iconbitmap(f'{main_path}/Data/img/icon/icon.ico')

        def fast_mode():
            self.img_load_mode = Image.NEAREST
            img_fast_mode_button.config(fg='green')
            img_hd_mode_button.config(fg='#000000')
            self.img_load_mode_info = '???????????? (Image.NEAREST)'

        def hd_mode():
            self.img_load_mode = Image.ANTIALIAS
            img_hd_mode_button.config(fg='green')
            img_fast_mode_button.config(fg='#000000')
            self.img_load_mode_info = '???????????? (Image.ANTIALIAS)'

        def local_mode():
            ask_img_file_path = askopenfilename(title='?????????????????????')
            if ask_img_file_path:
                self.now_file_path = ask_img_file_path
                self.acquired_mode = 'local'
                self.now_file_dir = dirname(self.now_file_path)
                now_file_dir_list = listdir(self.now_file_dir)
                self.now_file_dir_list.clear()
                for file_name in now_file_dir_list:
                    file_name_suffix = file_name.split('.')[-1].upper()
                    if file_name_suffix in self.support_type:
                        self.now_file_dir_list.append(file_name)
                self.now_file_dir_list_len = len(self.now_file_dir_list)

                local_mode_button.config(fg='green')
                web_mode_button.config(fg='#000000')
                self.log_out('?????????????????? :', self.now_file_dir_list)
                self.log_out(' | ??????????????????????????????: ', self.now_file_dir)
                self.log_out(' <!> ???????????????????????????', level='WARNING')
            else:
                self.log_out(' <!> ???????????????????????????', level='WARNING')

        def web_mode():
            self.acquired_mode = 'web'
            web_mode_button.config(fg='green')
            local_mode_button.config(fg='#000000')
            self.log_out(' <!> ???????????????????????????', level='WARNING')

        def set_random():
            self.switch = 'random'
            random_button.config(fg='green')
            order_button.config(fg='#000000')
            order_button.deselect()
            self.log_out('<!> ????????????????????????', level='WARNING')

        def set_order():
            self.switch = 'order'
            order_button.config(fg='green')
            random_button.config(fg='#000000')
            random_button.deselect()
            self.log_out('<!> ????????????????????????', level='WARNING')

        def set_switch_interval():
            ent_switch_interval = switch_interval_ent.get()
            if self.is_int(ent_switch_interval):
                self.switch_interval = int(ent_switch_interval)
                switch_interval_ent.config(fg='#000000')
                self.log_out('<!> ??????????????????????????????????????? %d (???)' % self.switch_interval, level='WARNING')
                if not self.auto_switch_running:
                    self.auto_switch()
            elif ent_switch_interval == '':
                switch_interval_ent.delete(0, tkinter.END)
                switch_interval_ent.insert(0, str(self.switch_interval))
                switch_interval_ent.config(fg='#000000')
            else:
                self.switch_interval = 'STOP'
                switch_interval_ent.delete(0, tkinter.END)
                switch_interval_ent.insert(0, 'STOP')
                switch_interval_ent.config(fg='red')

        def set_switch_wallpaper():
            self.switch_wallpaper = not self.switch_wallpaper
            if self.switch_wallpaper:
                switch_w_button.config(text='??????')
                switch_w_label.config(fg='green')
                Thread(target=lambda: self.wallpaper()).start()
                self.log_out('<!> ????????????????????????', level='WARNING')
            else:
                switch_w_button.config(text='??????')
                switch_w_label.config(fg='red')
                self.log_out('<!> ????????????????????????', level='WARNING')

        def set_external_viewer():
            self.default_external_viewer = not self.default_external_viewer
            if self.default_external_viewer:
                external_viewer_button.config(text='??????')
                external_viewer_label.config(fg='green')
                self.log_out('<!> ?????????????????????????????????', level='WARNING')
            else:
                external_viewer_button.config(text='??????')
                external_viewer_label.config(fg='red')
                self.log_out('<!> ?????????????????????????????????', level='WARNING')

        def set_history_count_max():
            history_count_get = history_count_ent.get()
            if self.is_int(history_count_get):
                self.history_count_max = int(history_count_get)
                if self.history_count_max == 0:
                    history_count_ent.config(fg='red')
                else:
                    history_count_ent.config(fg='#000000')
            else:
                self.log_out('<!> ????????????????????????????????????????????????', level='ERROR')
                history_count_ent.delete(0, tkinter.END)
                history_count_ent.insert(0, str(self.history_count_max))

        def set_auto_save():
            self.auto_save_do = not self.auto_save_do
            if self.auto_save_do:
                new_path = askdirectory(
                    title='????????????????????????', initialdir=f'{main_path}/Data/img/')
                if new_path:
                    self.auto_save_dir = new_path
                    self.log_out('<!> ????????????????????? :', new_path, level='WARNING')
                    auto_save_label.config(fg='green')
                    auto_save_button.config(text='??????')
                else:
                    self.log_out('<!> ???????????????????????????', level='WARNING')
                    self.auto_save_do = not self.auto_save_do
                    auto_save_label.config(fg='#000000')
            else:
                self.log_out('<!> ?????????????????????', level='WARNING')
                auto_save_label.config(fg='red')
                auto_save_button.config(text='??????')

        def set_bg_color():
            color: Tuple[Tuple[float, float, float], str] = askcolor('#000000')
            if color[0]:
                self.ask_color_all = color
                self.wallpaper_bg_color = color[0]
                bg_color_label.config(bg=color[1])
                self.log_out('<!> ???????????????????????????????????????', level='WARNING')
            else:
                self.log_out('<!> ???????????????????????????????????????', level='WARNING')

        def change_config():
            ask_config_file_path = askopenfilename(title='?????????????????????',
                                                   filetypes=[('JSON', '*.json'), ('Any-Type', '*')],
                                                   initialdir=dirname(self.now_config_file_path),
                                                   initialfile=basename(self.now_config_file_path))
            old_config_file_path = self.now_config_file_path
            if exists(ask_config_file_path):
                def _not_ok():
                    self.now_config_file_path = old_config_file_path
                    config_path_text_button.config(fg='red')
                    config_path_text_button.after(ms=5000, func=lambda: config_path_text_button.config(fg='#000000'))

                self.now_config_file_path = ask_config_file_path
                try:
                    self.config_refresh()
                except UnicodeDecodeError:
                    self.log_out('<!> ??????????????????, ???????????????!', level='ERROR')
                    _not_ok()
                except json.decoder.JSONDecodeError:
                    self.log_out('<!> ??????????????????, ???????????????!', level='ERROR')
                    _not_ok()
                except KeyError:
                    self.log_out('<!> ??????????????????, ???????????????!', level='ERROR')
                    _not_ok()
                else:
                    config_path_text_button.delete(1.0, tkinter.END)
                    config_path_text_button.insert(1.0, self.now_config_file_path)

        def set_run_log():
            self.run_log = not self.run_log
            if self.run_log:
                self.log_out('<!> ????????????!', level='WARNING')
                run_log_button.config(text='????????????', fg='green')
            else:
                self.log_out('<!> ????????????!', level='WARNING')
                run_log_button.config(text='????????????', fg='red')

        tkinter.Label(master=post_win, text='??????????????????').pack()
        check_frame1 = tkinter.Frame(master=post_win)
        img_fast_mode_button = tkinter.Button(master=check_frame1, text='????????????', command=fast_mode)
        img_fast_mode_button.pack(side=tkinter.LEFT, padx=5)
        img_hd_mode_button = tkinter.Button(master=check_frame1, text='????????????', command=hd_mode)
        img_hd_mode_button.pack(side=tkinter.LEFT, padx=5)
        if self.img_load_mode == Image.NEAREST:
            img_fast_mode_button.config(fg='green')
        else:
            img_hd_mode_button.config(fg='green')
        check_frame1.pack()

        tkinter.Label(master=post_win, text='??????????????????').pack()
        check_frame2 = tkinter.Frame(master=post_win)
        local_mode_button = tkinter.Button(master=check_frame2, text='????????????', command=local_mode)
        local_mode_button.pack(side=tkinter.LEFT, padx=5)
        web_mode_button = tkinter.Button(master=check_frame2, text='????????????', command=web_mode)
        web_mode_button.pack(side=tkinter.LEFT, padx=5)
        if self.acquired_mode == 'web':
            web_mode_button.config(fg='green')
        else:
            local_mode_button.config(fg='green')
        check_frame2.pack()

        check_frame3 = tkinter.Frame(master=post_win)
        random_button = tkinter.Checkbutton(
            master=check_frame3, text='????????????', command=set_random)
        order_button = tkinter.Checkbutton(
            master=check_frame3, text='????????????', command=set_order)
        random_button.pack(side=tkinter.LEFT, padx=5)
        order_button.pack(side=tkinter.LEFT, padx=5)
        check_frame3.pack()
        if self.switch == 'order':
            order_button.config(fg='green')
            order_button.select()
        else:
            random_button.config(fg='green')
            random_button.select()

        tkinter.Button(master=post_win, text='??????????????????',
                       command=self.data_refresh).pack(ipadx=5)

        switch_interva_frame = tkinter.Frame(master=post_win)
        tkinter.Label(master=switch_interva_frame,
                      text='??????????????????(s)').pack(side=tkinter.LEFT)
        switch_interval_ent = tkinter.Entry(
            master=switch_interva_frame, width=6)
        switch_interval_ent.delete(0, 'end')
        switch_interval_ent.insert(0, str(self.switch_interval))
        switch_interval_ent.pack(side=tkinter.LEFT)
        tkinter.Button(master=switch_interva_frame, text='??????',
                       command=set_switch_interval, ).pack(side=tkinter.LEFT)
        switch_interva_frame.pack()

        check_frame5 = tkinter.Frame(master=post_win)
        switch_w_label = tkinter.Label(master=check_frame5, text='??????????????????',
                                       fg='green' if self.switch_wallpaper else 'red')
        switch_w_label.pack(side=tkinter.LEFT)
        switch_w_button = tkinter.Button(master=check_frame5, text='??????' if not self.switch_wallpaper else '??????',
                                         command=set_switch_wallpaper)

        switch_w_button.pack(side=tkinter.LEFT, padx=5)
        external_viewer_label = tkinter.Label(master=check_frame5, text='??????????????????',
                                              fg='green' if self.default_external_viewer else 'red')
        external_viewer_label.pack(side=tkinter.LEFT)
        external_viewer_button = tkinter.Button(master=check_frame5,
                                                text='??????' if not self.default_external_viewer else '??????',
                                                command=set_external_viewer)
        external_viewer_button.pack(side=tkinter.LEFT, padx=5)
        check_frame5.pack()
        # history
        history_frame = tkinter.Frame(master=post_win)
        tkinter.Button(master=history_frame, text='??????????????????',
                       command=lambda: startfile(self.history_save_dir)).pack(side=tkinter.TOP, padx=5)
        tkinter.Label(master=history_frame, text='??????????????????????????????').pack(
            side=tkinter.LEFT)
        history_count_ent = tkinter.Entry(master=history_frame, width=6)
        history_count_ent.select_clear()
        history_count_ent.insert(0, string=str(self.history_count_max))
        history_count_ent.pack(side=tkinter.LEFT)
        tkinter.Button(master=history_frame, text='??????',
                       command=set_history_count_max, ).pack(side=tkinter.LEFT)
        history_frame.pack()

        # auto save
        auto_save_frame = tkinter.Frame(master=post_win)
        auto_save_label = tkinter.Label(master=auto_save_frame, text='????????????',
                                        fg='green' if self.auto_save_do else 'red')
        auto_save_label.pack(side=tkinter.LEFT)
        auto_save_button = tkinter.Button(master=auto_save_frame, text='??????' if not self.auto_save_do else '??????',
                                          command=set_auto_save)
        auto_save_button.pack(side=tkinter.LEFT, padx=5)
        auto_save_frame.pack()

        # bg color
        bg_color_frame = tkinter.Frame(master=post_win)
        tkinter.Label(master=bg_color_frame, text='????????????????????????').pack(
            side=tkinter.LEFT)
        bg_color_button = tkinter.Button(master=bg_color_frame, text='????????????',
                                         command=set_bg_color)
        bg_color_button.pack(side=tkinter.LEFT, padx=5)
        bg_color_label = tkinter.Label(
            master=bg_color_frame, bg=self.ask_color_all[1], width=5)
        bg_color_label.pack(side=tkinter.LEFT, padx=5)
        bg_color_frame.pack()

        # change config
        change_config_frame = tkinter.Frame(master=post_win)
        config_path_text_button = tkinter.Text(master=change_config_frame,
                                               font=('Microsoft Yahei Mono', 10), height=1, width=25)
        config_path_text_button.delete(1.0, tkinter.END)
        config_path_text_button.insert(1.0, self.now_config_file_path)
        config_path_text_button.pack(side=tkinter.LEFT)
        config_path_button = tkinter.Button(master=change_config_frame, text='??????????????????',
                                            command=change_config)
        config_path_button.pack(side=tkinter.LEFT)
        change_config_frame.pack()

        # run log
        run_log_frame = tkinter.Frame(master=post_win)
        run_log_button = tkinter.Button(master=run_log_frame, text='????????????' if self.run_log else '????????????',
                                        fg='green' if self.run_log else 'red', command=set_run_log)
        open_log_dir_button = tkinter.Button(master=run_log_frame, text='??????????????????',
                                             command=lambda: startfile(f'{main_path}/log'))
        run_log_button.pack(side=tkinter.LEFT)
        open_log_dir_button.pack(side=tkinter.LEFT)
        run_log_frame.pack()

        def del_win():
            post_win.quit()
            post_win.destroy()
            self.have_set_up_win = False

        post_win.protocol('WM_DELETE_WINDOW', del_win)
        post_win.mainloop()

    def web_refresh(self, key):
        if key in self.request_datas:
            self.request_data = self.request_datas[key]
        else:
            self.request_data = None
        if key in self.response_processing_dict:
            self.response_processing = self.response_processing_dict[key]
        else:
            self.response_processing = None
        if key in self.request_params_dict:
            self.request_params = self.request_params_dict[key]
        else:
            self.request_params = None
        if self.url in self.proxies_dict:
            self.proxies: dict = self.proxies_dict[key]
        else:
            self.proxies = None

    def show_web_info(self):
        self.log_out(' | ??????API?????? :', self.url)
        self.log_out(' | ?????????????????? :', self.now_img_url)
        self.log_out(' | ??????API?????? :', self.now_url_index)
        self.log_out(' | ?????????????????? :', self.request_params)
        self.log_out(' | ?????????????????? :', self.request_data)
        self.log_out(' | ?????????????????? :', self.proxies)
        self.log_out('??????' * 25)

    def switch_url(self):
        if self.acquired_mode == 'web':
            if self.switch == 'random':
                self.url = sample(self.urls, 1)[0]
                self.show_web_info()
                random_key = self.url
                self.web_refresh(key=random_key)

            elif self.switch == 'order':
                self.now_url_index = self.now_url_index + 1
                if self.now_url_index == self.urls_len:
                    self.now_url_index = 0
                self.show_web_info()
                self.url = self.urls[self.now_url_index]
                now_key = self.url
                self.web_refresh(key=now_key)

        elif self.acquired_mode == 'local':
            if self.switch == 'random':
                now_files_len = self.now_file_dir_list_len
                now_files_name = self.now_file_dir_list[randint(
                    0, now_files_len - 1)]
                self.log_out(' | ?????????????????? :', now_files_name)
                self.log_out(' | ?????????????????? :', self.now_file_dir)
                self.log_out('??????' * 25)
                self.now_file_path = join(self.now_file_dir, now_files_name)
            elif self.switch == 'order':
                now_file_name = basename(self.now_file_path)
                now_file_index = self.now_file_dir_list.index(now_file_name)
                if now_file_index == len(self.now_file_dir_list) - 1:
                    now_file_index = 0
                next_file = self.now_file_dir_list[now_file_index + 1]
                self.log_out(' | ?????????????????? :', next_file)
                self.log_out(' | ?????????????????? :', self.now_file_dir)
                self.log_out('??????' * 25)
                self.now_file_path = join(self.now_file_dir, next_file)


if __name__ == '__main__':
    app = GetImgAPI()
    app.run()
