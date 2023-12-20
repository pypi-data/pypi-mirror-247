import os
import shutil
import base64
from pyecharts.charts import Bar, Line, Scatter, Pie, Radar, Grid, Timeline
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_ECHARTS_JS = os.path.join(BASE_DIR, "js/echarts.min.js")

# print(BASE_DIR)
CurrentConfig.GLOBAL_ENV.loader.searchpath = [os.path.join(BASE_DIR, "templates")]


def _transform_image_to_html(image):
    if not image.startswith("http"):
        with open(image, "rb") as fp:
            content = fp.read()
        seps = image.split(".")
        sep = "png"
        if len(seps) > 0:
            sep = seps[-1]
        image = f"data:image/{sep};base64," + base64.b64encode(content).decode("utf-8")

    return image


class ChartBase:

    def set_theme(self, theme):
        """
        设置图表主题
        :param theme: 字符串，图表主题
        :return: self
        """
        self._obj.theme = theme
        return self

    def to_html(self, filename):
        """
        导出图表到html文件
        :param filename: 字符串，文件名，必填
        :return: self
        """
        # self._obj.js_host = "js/"
        # dst_dir = os.path.join(os.path.dirname(self._obj.render(filename)), self._obj.js_host)
        # if not os.path.exists(dst_dir):
        #     os.makedirs(dst_dir)
        # dst = os.path.join(dst_dir, "echarts.min.js")
        # shutil.copy(FILE_ECHARTS_JS, dst)
        with open(FILE_ECHARTS_JS, "r", encoding="utf-8") as fp:
            js_content = fp.read()
        self._obj.js_content = js_content
        self._obj.render_options.update(zyb_js=True)
        self._obj.render(filename)
        return self


class ChartObjMix(ChartBase):

    def get_obj(self):
        return self._obj

    def set_title(self, title, font_size=None, color=None):
        """
        设置图表标题
        :param title: 字符串，标题名称，必填
        :param font_size: 标题文字大小，选填
        :param color: 字符串，标题文字颜色
        :return: self
        """
        # 舍弃全局配置设置方式，全局设置方式会导致其他设置失效
        # self._obj.set_global_opts(
        #     title_opts=opts.TitleOpts(title=title,
        #                               title_textstyle_opts=opts.TextStyleOpts(
        #                                   color=color,
        #                                   font_size=font_size
        #                               ))
        # )
        self._obj.options.update(title=opts.TitleOpts(
            title=title,
            title_textstyle_opts=opts.TextStyleOpts(color=color,
                                                    font_size=font_size)))
        return self

    def set_legend(self, is_show=True):
        """
        设置图表图例
        :param is_show: 布尔值，是否显示图例
        :return: self
        """
        # self._obj.options.update(legend_opts=opts.LegendOpts(is_show=is_show))
        legend_opts = opts.LegendOpts(is_show=is_show).opts
        for _s in self._obj.options["legend"]:
            _s.update(**{k: v for k, v in legend_opts.items() if v is not None})
        return self

    def set_bg(self, image, width=None, height=None, opacity=1):
        """
        设置背景图
        :param image: 字符串，图片路径，必填
        :param width: 字符串，选填，背景图片宽
        :param height: 字符串，选填，背景图片高
        :param opacity: 浮点型，透明度，选填
        :return:
        """
        image = _transform_image_to_html(image)
        self._obj.options.update(graphic=opts.GraphicImage(
            graphic_item=opts.GraphicItem(z=-10),
            graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                image=image,
                width=width,
                height=height,
                opacity=opacity
            )
        ))

        return self


class Common:
    """
    常用图基类
    """

    def add_x(self, data):
        """
        添加x轴数据
        :param data: 列表， X轴数据，必填
        :param name: 字符串，X轴标签名称，非必填，默认为空
        :return: 图表对象本身 self
        """
        self._obj.add_xaxis(data)
        return self

    def add_y(self, data, name="", index=0):
        """
        添加Y轴数据
        :param data: 列表，对应x轴标签的数据值, 必填
        :param name:字符串，图例名称, 非必填，默认为空
        :param index: 整型，Y轴索引,非必填，默认为0，即图表原始Y轴，结合拓展轴(extend)会有索引为1，即引用拓展轴
        :return: 图像本身
        """
        self._obj.add_yaxis(name, data, yaxis_index=index)
        return self

    def extend(self, minvalue=0, maxvalue=None, interval=None):
        """
        扩展坐标轴
        :param minvalue: 整型或浮点型，最小刻度，非必填默认0
        :param maxvalue: 整型或浮点型，最大刻度，非必填，默认为引用轴的数据上线
        :param interval: 整型或浮点型，最大刻度，非必填
        :return:
        """
        if not isinstance(minvalue, (int, float)):
            raise ValueError("minvalue数据类型错误")
        if not isinstance(maxvalue, (int, float)):
            raise ValueError("maxvalue数据类型错误")
        if interval and not isinstance(interval, (int, float)):
            raise ValueError("interval数据类型错误")

        self._obj.extend_axis(
            yaxis=opts.AxisOpts(
                min_=minvalue,
                max_=maxvalue,
                interval=interval
            )
        )
        return self

    def extend_x(self, minvalue=0, maxvalue=None, interval=None):
        """
        扩展x坐标轴
        :param minvalue: 整型或浮点型，最小刻度，非必填默认0
        :param maxvalue: 整型或浮点型，最大刻度，非必填，默认为引用轴的数据上线
        :param interval:
        :return:
        """
        if not isinstance(minvalue, (int, float)):
            raise ValueError("minvalue数据类型错误")
        if not isinstance(maxvalue, (int, float)):
            raise ValueError("maxvalue数据类型错误")
        if interval and not isinstance(interval, (int, float)):
            raise ValueError("interval数据类型错误")

        self._obj.extend_axis(
            xaxis=opts.AxisOpts(
                min_=minvalue,
                max_=maxvalue,
                interval=interval
            )
        )
        return self

    def reversal(self):
        """
        坐标轴翻转
        :return: self
        """
        self._obj.reversal_axis()
        return self

    def set_axis(self, is_show):
        """
        设置图表坐标轴
        :param is_show: 布尔型，是否显示坐标轴，必填，True显示，False不显示
        :return: self
        """
        if not isinstance(is_show, bool):
            raise ValueError("参数类型错误")
        xaxis_opts = opts.AxisOpts(is_show=is_show)
        yaxis_opts = opts.AxisOpts(is_show=is_show)

        if self._obj.options.get("xAxis", None):
            xaxis_opts = xaxis_opts.opts
            self._obj.options["xAxis"][0].update(xaxis_opts)

        if self._obj.options.get("yAxis", None):
            yaxis_opts = yaxis_opts.opts
            self._obj.options["yAxis"][0].update(yaxis_opts)
        return self


class ZybBar(Common, ChartObjMix):
    """
    柱状图类
    """

    def __init__(self):
        super(ZybBar, self).__init__()
        self._obj = Bar()

    def set_label(self, position='top', formatter='{b}:{d}%', color='black'):
        """
        设置图条标签
        :param position: 字符串，标签位置，选填
        :param formatter: 字符串，标签显示格式，选填
        :param color: 字符串，标签显示颜色，选填
        :return:
        """
        self._obj.set_series_opts(label_opts=opts.LabelOpts(
            position=position,
            formatter=formatter,
            color=color
        ))


class ZybLine(Common, ChartObjMix):
    """
    折线图类
    """

    def __init__(self):
        super(ZybLine, self).__init__()
        self._obj = Line()


class ZybScatter(Common, ChartObjMix):
    """
    散点图类
    """

    def __init__(self):
        super(ZybScatter, self).__init__()
        self._obj = Scatter()

    def set_axis(self, is_show, type_x='value'):
        """
        设置图表坐标轴
        :param is_show: 布尔型，是否显示坐标轴，必填，True显示，False不显示
        :param type_x: 字符串，x轴类别，选填
        :return: self
        """
        if not isinstance(is_show, bool):
            raise ValueError("参数类型错误")

        xaxis_opts = opts.AxisOpts(is_show=is_show, type_=type_x, is_scale=True)
        yaxis_opts = opts.AxisOpts(is_show=is_show, type_=type_x, is_scale=True)

        if self._obj.options.get("xAxis", None):
            xaxis_opts = xaxis_opts.opts
            self._obj.options["xAxis"][0].update(xaxis_opts)

        if self._obj.options.get("yAxis", None):
            yaxis_opts = yaxis_opts.opts
            self._obj.options["yAxis"][0].update(yaxis_opts)

        return self


class ZybPie(ChartObjMix):
    """
    饼图类
    """

    def __init__(self):
        self._obj = Pie()

    def add(self, data):
        """
        添加数据
        :param data:二维列表， 图表数据，必填项
        :return:
        """
        self._obj.add("", data)
        return self

    def set_radius(self, in_radius, out_radius):
        """
        设置半径
        :param in_radius: 整型或浮点型，内径，必填
        :param out_radius: 整型或浮点型，外径，必填
        :return: self
        """
        if not isinstance(in_radius, (float, int)):
            raise ValueError("in_radius参数错误")
        if not isinstance(out_radius, (float, int)):
            raise ValueError("out_radius参数错误")
        # for series in self._obj.options.get("series", []):
        #     series['radius'] = [in_radius, out_radius]
        self._obj.set_series_opts(radius=[in_radius, out_radius])
        return self

    def set_center(self, x=None, y=None):
        """
        设置中心
        :param x: 整型或浮点型，横坐标，选填
        :param y: 整型或浮点型，横坐标，选填
        :return: self
        """
        if x is not None and not isinstance(x, (int, float)):
            raise ValueError("x参数错误")
        elif x is None:
            x = '50%'
        if y is not None and not isinstance(y, (int, float)):
            raise ValueError("y参数错误")
        elif y is None:
            y = '50%'

        # for series in self._obj.options.get("series", []):
        #     series['center'] = [x, y]
        self._obj.set_series_opts(center=[x, y])
        return self

    def set_style(self, shape=None):
        """
        设置样式
        :param shape: 字符串，选填
        """
        if shape and not isinstance(shape, str):
            raise ValueError("shape参数类型错误")
        # for series in self._obj.options.get("series", []):
        #     series['roseType'] = shape
        self._obj.set_series_opts(roseType=shape)
        return self

    def set_formatter(self, f='{b}:{d}%'):
        """
        设置饼图标签格式
        :param f: 字符串，饼图形状， 选填
        :return:
        """
        self._obj.set_series_opts(label_opts=opts.LabelOpts(formatter=f))


class ZybRadar(ChartObjMix):
    """
    雷达图类
    """

    def __init__(self):
        self._obj = Radar()

    def add(self, data):
        """
        添加数据
        :param data: 二维列表，图表数据，必填
        :return: self
        """
        self._obj.add("", data)
        return self

    def set_schema(self, name=None, color=None):
        """
        设置刚要
        :param name: 列表，雷达图各个纬度名称，选填
        :param color: 列表，雷达图各个纬度颜色，选填
        :return: self
        """
        if name and not isinstance(name, list):
            raise ValueError("参数name数据错误")
        if color and not isinstance(color, list):
            raise ValueError("参数name数据错误")
        if not name and not color:
            return
        if not name:
            name = []
        if not color:
            color = []
        len_name = len(name)
        len_color = len(color)
        max_length = max([len_name, len_color])

        new_indicators = []
        for i in range(max_length):
            item = {}
            if i < len_name:
                item['name'] = name[i]
            else:
                item['name'] = ""
            if i < len_color:
                item['color'] = color[i]
            else:
                item['color'] = ""
            item["min"] = 0
            new_indicators.append(item)

        indicators = self._obj.options.get("radar", [])
        if not indicators:
            self._obj.add_schema(new_indicators)
        else:
            for indicator in indicators:
                for i, j in indicator["indicator"]:
                    if i < len_name:
                        j['name'] = name[i]
                    if i < len_color:
                        j['color'] = color[i]
                    if i >= max_length:
                        break
        return self

    def set_schema_limit(self, minvalue=None, maxvalue=None):
        """
        设置纲要范围
        :param minvalue: 列表，各个纬度的最小值，选填
        :param maxvalue: 列表，各个纬度的最大值，选填
        :return: self
        """
        if minvalue and not isinstance(minvalue, list):
            raise ValueError("参数name数据错误")
        if maxvalue and not isinstance(maxvalue, list):
            raise ValueError("参数name数据错误")
        if not maxvalue and not maxvalue:
            return
        if not minvalue:
            minvalue = []
        if not maxvalue:
            maxvalue = []
        len_min = len(minvalue)
        len_max = len(maxvalue)
        max_length = max([len_min, len_max])

        new_indicators = []
        for i in range(max_length):
            item = {}
            if i < len_min:
                item['min'] = minvalue[i]
            else:
                item['min'] = 0
            if i < len_max:
                item['max'] = maxvalue[i]
            new_indicators.append(item)

        indicators = self._obj.options.get("radar", [])
        if not indicators:
            self._obj.add_schema(new_indicators)
        else:
            for indicator in indicators:
                for i, j in enumerate(indicator["indicator"]):
                    if i < len_min:
                        j['min'] = minvalue[i]
                    if i < len_max:
                        j['max'] = maxvalue[i]
                    if i >= max_length:
                        break
        return self

    def set_style(self, shape=None):
        """
        设置样式
        :param shape: 字符串，雷达图底盘形状，选填
        """
        if shape and not isinstance(shape, str):
            raise ValueError("shape参数类型错误")
        for indicator in self._obj.options.get("radar", []):
            indicator['shape'] = shape
        return self


class ZybGrid(ChartObjMix):
    """
    并行多图类
    """

    def __init__(self):
        self._obj = Grid(init_opts=opts.InitOpts(width='1250px', height='550px', theme='white'))
        self._title = Line()
        self._title.set_global_opts(
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(is_show=False),
            legend_opts=opts.LegendOpts(is_show=False)
        )
        self._obj.add(self._title, opts.GridOpts(pos_bottom='100%'))

    def add(self, chart, position):
        """
        添加图表
        :param chart: 对象，载入网格中的图表对象，必填
        :param position: 列表，图表位置，列表中四个元素为字符串形式，顺时针表示[上,下,左,右]
        :return: self
        """
        if not hasattr(chart, 'get_obj'):
            raise ValueError("chart 为非图表对象")
        if not isinstance(position, list) or len(position) != 4:
            raise ValueError("position 数据错误")
        self._obj.add(chart.get_obj(), opts.GridOpts(pos_top=position[0],
                                                     pos_right=position[1],
                                                     pos_bottom=position[2],
                                                     pos_left=position[3]))
        return self

    def set_size(self, width='900px', height='500px'):
        """
        设置尺寸
        :param width: 字符串，网格宽度，选填
        :param height: 字符串，网格高度，选填
        :return: self
        """
        self._obj.width = width
        self._obj.height = height
        return self

    def set_bg(self, image, width=None, height=None, opacity=1):
        """
        设置背景图
        :param image: 字符串，图片路径，必填
        :param width: 字符串，选填，背景图片宽
        :param height: 字符串，选填，背景图片高
        :param opacity: 浮点型，透明度，选填
        :return:
        """
        image = _transform_image_to_html(image)
        self._obj.options.update(graphic=opts.GraphicImage(
            graphic_item=opts.GraphicItem(z=-10),
            graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                image=image,
                width=width,
                height=height,
                opacity=opacity
            )
        ))

        return self

    def set_title(self, title, font_size=30, color='black'):
        """
        设置标题
        :param title:
        :param font_size:
        :param color:
        :return:
        """
        titles = self._title.options.get("title")
        if titles:
            for opt in titles.opts:
                opt.update(text=title, left='44.5%', top='2%')
                if opt.get('textStyle'):
                    style = opt.get('textStyle')
                    style.update(font_size=font_size, color=color)
                else:
                    opt['textStyle'] = opts.TextStyleOpts(
                        font_size=font_size,
                        color=color
                    )
        else:
            self._title.options.update(
                title=opts.TitleOpts(
                    title=title, pos_left='44.5%', pos_top='2%',
                    title_textstyle_opts=opts.TextStyleOpts(
                        font_size=30
                    )
                )
            )
        return self


class ZybTimeline(ChartBase):
    """
    时序轮播轴
    """

    def __init__(self):
        self._obj = Timeline()

    def add(self, chart, name):
        """
        添加x轴数据
        :param name: 字符串，轮博轴标签，必填
        :param chart: 对象， 载入轮轴的图表对象或者网格对象
        :return: self
        """
        if not hasattr(chart, 'get_obj'):
            raise ValueError("chart 为非图表对象")
        if not isinstance(name, str):
            raise ValueError("name 数据错误")
        self._obj.add(chart.get_obj(), name)
        return self

    def set_schema(self, interval=1000, is_loop=True, is_auto=False):
        """
        设置提要
        :param interval: 整型或浮点型，时间间隔，单位毫秒，选填
        :param is_loop: 布尔，是否循环播放，选填，默认True
        :param is_auto: 布尔，是否自启动，选填，默认False
        :return: self
        """
        self._obj.add_schema(play_interval=interval, is_loop_play=is_loop, is_auto_play=is_auto)
        return self

    def set_size(self, width, height):
        """
        设置尺寸
        :param width: 字符串，轮播页宽度，选填，默认900px
        :param height: 字符串，轮播页高度，选填，默认500px
        :return: self
        """
        self._obj.width = width
        self._obj.height = height
        return self


