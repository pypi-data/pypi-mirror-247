import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from lcszh.hit_stopwords import stopwords
import os

import sys
if sys.version_info.major < 3 or sys.version_info.minor < 7:
    from wordcloud.wordcloud import itemgetter, Random, IntegralOccupancyMap, Image, ImageDraw, np, ImageFont
    def generate_from_frequencies(self, frequencies, max_font_size=None):  # noqa: C901
        """Create a word_cloud from words and frequencies.

        Parameters
        ----------
        frequencies : dict from string to float
            A contains words and associated frequency.

        max_font_size : int
            Use this font-size instead of self.max_font_size

        Returns
        -------
        self

        """
        # make sure frequencies are sorted and normalized
        frequencies = sorted(frequencies.items(), key=itemgetter(1), reverse=True)
        if len(frequencies) <= 0:
            raise ValueError("We need at least 1 word to plot a word cloud, "
                             "got %d." % len(frequencies))
        frequencies = frequencies[:self.max_words]

        # largest entry will be 1
        max_frequency = float(frequencies[0][1])

        frequencies = [(word, freq / max_frequency)
                       for word, freq in frequencies]

        if self.random_state is not None:
            random_state = self.random_state
        else:
            random_state = Random()

        if self.mask is not None:
            boolean_mask = self._get_bolean_mask(self.mask)
            width = self.mask.shape[1]
            height = self.mask.shape[0]
        else:
            boolean_mask = None
            height, width = self.height, self.width
        occupancy = IntegralOccupancyMap(height, width, boolean_mask)

        # create image
        img_grey = Image.new("L", (width, height))
        draw = ImageDraw.Draw(img_grey)
        img_array = np.asarray(img_grey)
        font_sizes, positions, orientations, colors = [], [], [], []

        last_freq = 1.

        if max_font_size is None:
            # if not provided use default font_size
            max_font_size = self.max_font_size

        if max_font_size is None:
            # figure out a good font size by trying to draw with
            # just the first two words
            if len(frequencies) == 1:
                # we only have one word. We make it big!
                font_size = self.height
            else:
                self.generate_from_frequencies(dict(frequencies[:2]),
                                               max_font_size=self.height)
                # find font sizes
                sizes = [x[1] for x in self.layout_]
                try:
                    font_size = int(2 * sizes[0] * sizes[1]
                                    / (sizes[0] + sizes[1]))
                # quick fix for if self.layout_ contains less than 2 values
                # on very small images it can be empty
                except IndexError:
                    try:
                        font_size = sizes[0]
                    except IndexError:
                        raise ValueError(
                            "Couldn't find space to draw. Either the Canvas size"
                            " is too small or too much of the image is masked "
                            "out.")
        else:
            font_size = max_font_size

        # we set self.words_ here because we called generate_from_frequencies
        # above... hurray for good design?
        self.words_ = dict(frequencies)

        if self.repeat and len(frequencies) < self.max_words:
            # pad frequencies with repeating words.
            times_extend = int(np.ceil(self.max_words / len(frequencies))) - 1
            # get smallest frequency
            frequencies_org = list(frequencies)
            downweight = frequencies[-1][1]
            for i in range(times_extend):
                frequencies.extend([(word, freq * downweight ** (i + 1))
                                    for word, freq in frequencies_org])

        # start drawing grey image
        for word, freq in frequencies:
            if freq == 0:
                continue
            # select the font size
            rs = self.relative_scaling
            if rs != 0:
                font_size = int(round((rs * (freq / float(last_freq))
                                       + (1 - rs)) * font_size))
            if random_state.random() < self.prefer_horizontal:
                orientation = None
            else:
                orientation = Image.ROTATE_90
            tried_other_orientation = False
            while True:
                # try to find a position
                font = ImageFont.truetype(self.font_path, font_size)
                # transpose font optionally
                transposed_font = ImageFont.TransposedFont(
                    font, orientation=orientation)
                # get size of resulting text
                box_size = draw.textsize(word, font=transposed_font)
                # find possible places using integral image:
                result = occupancy.sample_position(box_size[1] + self.margin,
                                                   box_size[0] + self.margin,
                                                   random_state)
                if result is not None or font_size < self.min_font_size:
                    # either we found a place or font-size went too small
                    break
                # if we didn't find a place, make font smaller
                # but first try to rotate!
                if not tried_other_orientation and self.prefer_horizontal < 1:
                    orientation = (Image.ROTATE_90 if orientation is None else
                                   Image.ROTATE_90)
                    tried_other_orientation = True
                else:
                    font_size -= self.font_step
                    orientation = None

            if font_size < self.min_font_size:
                # we were unable to draw any more
                break

            x, y = np.array(result) + self.margin // 2
            # actually draw the text
            draw.text((y, x), word, fill="white", font=transposed_font)
            positions.append((x, y))
            orientations.append(orientation)
            font_sizes.append(font_size)
            colors.append(self.color_func(word, font_size=font_size,
                                          position=(x, y),
                                          orientation=orientation,
                                          random_state=random_state,
                                          font_path=self.font_path))
            # recompute integral image
            if self.mask is None:
                img_array = np.asarray(img_grey)
            else:
                img_array = np.asarray(img_grey) + boolean_mask
            # recompute bottom right
            # the order of the cumsum's is important for speed ?!
            occupancy.update(img_array, x, y)
            last_freq = freq

        self.layout_ = list(zip(frequencies, font_sizes, positions,
                                orientations, colors))
        return self

    WordCloud.generate_from_frequencies = generate_from_frequencies


def word_cloud_diagram(text, diagram_path, self_words=None, stop_words=None, font_path=None, width=1500, height=600, background_color='white', imshow=True):
    """
        生成词云图的函数，将text的内容根据关键词生成词云图
    如：
        word_cloud_diagram('test.txt', 'ciyun.png', self_words=['工作狂人', '我爱工作'], stop_words=['吃饭', '睡觉', '上班'])
        将本地的test.txt文件生成词云图，并保存到ciyun.png，自己添加了 吃饭、睡觉、上班三个停用词
    :param txt_path: txt文本路径
    :param diagram_path: 词云图保存路径
    :param diagram_path: 词云图保存路径
    :param stop_words: list，自定义词库，默认已经使用哈工大停用词
    :param stop_words: list，自定义停用词，默认已经使用哈工大停用词
    :param text: str，文本字符串
    :param diagram_path: 词云图保存路径，如'a.png'
    :param stop_words: list，自定义停用词，默认已经使用哈工大停用词
    :param font_path: 字体路径，模型使用微软雅黑，字体通常在 'c:/windows/fonts' 目录下
    :param width: int，词云图的宽
    :param height: int，词云图的高
    :param background_color: 背景颜色，如'white'
    :param imshow: 是否显示图片，默认显示
    :return: dict，词云图中所有的词，按照权重大小排序的结果，key为词，value为权重
            data_cut:分词后的所有词
    """

    if font_path is None:
        font_path = os.path.abspath(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "msyh.ttc"))

    if isinstance(stop_words, list):
        for s in stop_words:
            if s not in stopwords:
                stopwords.append(s)

    if self_words is not None:
        for word in self_words:
            jieba.add_word(word)

    data_cut = jieba.lcut(text, cut_all=False)

    data_result = []
    for i in data_cut:
        if i not in stopwords:
            data_result.append(i)
    text = " ".join(data_result).replace("\n", " ")

    # 生成对象
    wc = WordCloud(font_path=font_path, width=width, height=height, mode="RGBA", background_color=background_color).generate(text)

    # 保存词云图
    wc.to_file(diagram_path)
    # 显示词云图
    if imshow:
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    return wc.words_, data_cut

