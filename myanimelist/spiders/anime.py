# -*- coding: utf-8 -*-
import scrapy
import re
import os

from myanimelist.items import AnimeItem

url_prefix = "https://myanimelist.net/anime/{}"


class AnimeSpider(scrapy.Spider):
    name = 'anime'

    # 只针对这个Spider的配置用custom_settings
    custom_settings = {
        # 是否使用配置文件设置要爬的anime_id
        # "LOAD_ANIME_ID_FROM_FILE": True
        "LOAD_ANIME_ID_FROM_FILE": False
    }

    allowed_domains = ['myanimelist.net']
    # start_urls = [url_prefix.format(i) for i in range(35790, 35791)]
    start_urls = [url_prefix.format(i) for i in range(1, 40000)]
    # start_urls = [url_prefix.format(i) for i in range(4015, 4016)]
    # start_urls = [url_prefix.format(i) for i in range(1298, 1299)]

    # 重写start_requests方法
    def start_requests(self):
        # 默认url使用start_urls
        url_list = self.start_urls
        load_anime_id_from_file = self.settings.get('LOAD_ANIME_ID_FROM_FILE', False)
        # 如果load_anime_id_from_file设置为true，使用配置文件的animeId
        if load_anime_id_from_file:
            try:
                url_list_from_file = []
                # 获取当前文件路径
                current_path = os.path.abspath(__file__)
                # 获取当前文件的父目录
                father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
                # 父目录的父目录 与anime_id_config.txt拼接
                config_file_path = os.path.join(os.path.abspath(os.path.dirname(father_path)), 'anime_id_config.txt')
                with open(config_file_path, 'r') as f:
                    lines = f.readlines()
                for i in range(0, len(lines)):
                    anime_id = lines[i].rstrip('\n')
                    url_from_file = url_prefix.format(anime_id)
                    url_list_from_file.append(url_from_file)
                url_list = url_list_from_file
            except:
                pass
        for url in url_list:
            yield self.make_requests_from_url(url)

    # 重写make_requests_from_url方法
    def make_requests_from_url(self, url):
        self.logger.debug('Try first time')
        return scrapy.Request(url=url, meta={'download_timeout': 10}, callback=self.parse, dont_filter=False)

    def parse(self, response):
        # 注意如果有tbody元素直接忽略
        sel = response.xpath('//div[@id="content"]/table/tr')
        # 虽然是extract()[0]取第一个元素，但是每次yield之后就会自动取下一个元素
        item = AnimeItem()
        try:
            item['pic'] = sel.xpath('td[1]/div/div[1]/a/img/@src').extract()[0]
        except:
            pass
        try:
            item['animeId'] = sel.xpath('td[1]/div/div[3]/input[@id="myinfo_anime_id"]/@value').extract()[0]
        except:
            pass
        try:
            enName_array = sel.xpath('td[1]/div/div[6]/text()').extract()
            item['enName'] = ''.join(enName_array).strip()
        except:
            pass
        # 有些动画页会多了一个Synonyms:属性
        title7 = sel.xpath('td[1]/div/div[7]/span/text()').extract()[0]
        extra = 0
        if title7 != 'Japanese:':
            extra = 1
        try:
            jpname_index = bytes(7 + extra)
            jpname_array = sel.xpath('td[1]/div/div['+jpname_index+']/text()').extract()
            item['jpName'] = ''.join(jpname_array).strip()
        except:
            pass
        try:
            type_index = bytes(8 + extra)
            item['type'] = sel.xpath('td[1]/div/div['+type_index+']/a/text()').extract()[0]
        except:
            pass
        try:
            episodes_index = bytes(9 + extra)
            episodes_array = sel.xpath('td[1]/div/div['+episodes_index+']/text()').extract()
            item['episodes'] = ''.join(episodes_array).strip()
        except:
            pass
        premiered_index = bytes(12 + extra)
        # 剧场版等的是没有Premiered和Premiered属性的，所以匹配下标要兼容
        title12 = sel.xpath('td[1]/div/div['+premiered_index+']/span/text()').extract()[0]
        producers_index = bytes(14 + extra)
        studios_index = bytes(16 + extra)
        source_index = bytes(17 + extra)
        if title12 == 'Premiered:':
            try:
                item['premiered'] = sel.xpath('td[1]/div/div['+premiered_index+']/a/text()').extract()[0]
            except:
                pass
        else:
            producers_index = bytes(12 + extra)
            studios_index = bytes(14 + extra)
            source_index = bytes(15 + extra)
            try:
                aired_index = bytes(11 + extra)
                aired_array = sel.xpath('td[1]/div/div['+aired_index+']/text()').extract()
                item['premiered'] = ''.join(aired_array).strip()
            except:
                pass
        try:
            producerArray = sel.xpath('td[1]/div/div['+producers_index+']/a/text()').extract()
            item['producers'] = ','.join(producerArray).strip()
        except:
            pass
        try:
            studioArray = sel.xpath('td[1]/div/div['+studios_index+']/a/text()').extract()
            item['studios'] = ','.join(studioArray).strip()
        except:
            pass
        try:
            sourceArray = sel.xpath('td[1]/div/div['+source_index+']/text()').extract()
            item['source'] = ''.join(sourceArray).strip()
        except:
            pass
        # 主题曲
        themeSongSel = sel.xpath('td[2]/div[1]/table/tr[2]/td[1]/div[3]')
        themeSongs = []
        try:
            openingThemeDetailList = themeSongSel.xpath('div[1]/div/span/text()').extract()
            openingThemeDetailList2 = themeSongSel.xpath('div[1]/div/div/span/text()').extract()
            openingThemeDetailList += openingThemeDetailList2
            for openingThemeDetail in openingThemeDetailList:
                animeThemeSong = AnimeThemeSong()
                animeThemeSong.setType('op')
                try:
                    songNameList = re.findall(r"\"(.+)\" by", openingThemeDetail)
                    animeThemeSong.setName(songNameList[0])
                    tempList = re.findall(r"\" by (.+)", openingThemeDetail)
                    # 用（划分，为了把演唱者抠出来
                    tempList2 = re.split('\\(+', tempList[0])
                    singer = ''
                    if (len(tempList2) > 2):
                        singer = (tempList2[0] + '(' + tempList2[1]).strip()
                    else:
                        singer = tempList2[0].strip()
                    animeThemeSong.setSinger(singer)
                except:
                    pass
                themeSongs.append(animeThemeSong)
        except:
            pass
        try:
            endingThemeDetailList = themeSongSel.xpath('div[3]/div/span/text()').extract()
            endingThemeDetailList2 = themeSongSel.xpath('div[3]/div/div/span/text()').extract()
            endingThemeDetailList += endingThemeDetailList2
            for endingThemeDetail in endingThemeDetailList:
                animeThemeSong = AnimeThemeSong()
                animeThemeSong.setType('ed')
                try:
                    songNameList = re.findall(r"\"(.+)\" by", endingThemeDetail)
                    animeThemeSong.setName(songNameList[0])
                    tempList = re.findall(r"\" by (.+)", endingThemeDetail)
                    # 用（划分，为了把演唱者抠出来
                    tempList2 = re.split('\\(+', tempList[0])
                    singer = ''
                    if (len(tempList2) > 2):
                        singer = (tempList2[0] + '(' + tempList2[1]).strip()
                    else:
                        singer = tempList2[0].strip()
                    animeThemeSong.setSinger(singer)
                except:
                    pass
                themeSongs.append(animeThemeSong)
        except:
            pass
        item['themeSongs'] = themeSongs

        # 根据内页地址爬取
        tab_list = sel.xpath('td[2]/div[1]/div[1]/ul[1]/li/a/text()').extract()
        characters_staff_url = ''
        for tab_index in range(len(tab_list)):
            if tab_list[tab_index] == 'Characters & Staff':
                tab_index_str = bytes(tab_index + 1)
                characters_staff_url = sel.xpath('td[2]/div[1]/div[1]/ul[1]/li[' + tab_index_str + ']/a/@href').extract()[0]
                break
        yield scrapy.Request(characters_staff_url, meta={'item': item}, callback=self.characters_staff_parse)

    def characters_staff_parse(self, response):
        # 接收上级已爬取的数据
        item = response.meta['item']
        #角色和staff页数据提取
        sel = response.xpath('//div[@id="content"]/table/tr')
        characters = []
        staffs = []
        try:
            name_list = sel.xpath('td[2]/div[1]/table/tr/td[2]/a/text()').extract()
            for index in range(len(name_list)):
                try:
                    name = name_list[index]
                    indexStr = bytes(index + 1)
                    role = sel.xpath('td[2]/div[1]/table['+indexStr+']/tr/td[2]/div/small/text()').extract()[0]
                    if role == 'Main' or role == 'Supporting':
                        animeCharacter = AnimeCharacter()
                        animeCharacter.setCharacterName(name)
                        animeCharacter.setType(role)
                        animeCharacter.setVoiceActor('')
                        try:
                            voice_actor_list = sel.xpath('td[2]/div[1]/table['+indexStr+']/tr/td[3]/table/tr/td/a/text()').extract()
                            for sub_index in range(len(voice_actor_list)):
                                voice_actor = voice_actor_list[sub_index]
                                sub_index_str = bytes(sub_index + 1)
                                nationality = sel.xpath('td[2]/div[1]/table[' + indexStr + ']/tr/td[3]/table/tr[' + sub_index_str + ']/td/small/text()').extract()[0]
                                if nationality == 'Japanese':
                                    animeCharacter.setVoiceActor(voice_actor)
                                    break
                        except:
                            pass
                        characters.append(animeCharacter)
                    else:
                        animeStaff = AnimeStaff()
                        animeStaff.setName(name)
                        animeStaff.setRoles(role)
                        staffs.append(animeStaff)
                except:
                    pass
        except:
            pass
        item['characters'] = characters
        item['staffs'] = staffs
        print(item)
        yield item


class AnimeCharacter():
    def setCharacterName(self, characterName):
        self.characterName = characterName
    def setType(self, type):
        self.type = type
    def setVoiceActor(self, voiceActor):
        self.voiceActor = voiceActor


class AnimeStaff():
    def setName(self, name):
        self.name = name
    def setRoles(self, roles):
        self.roles = roles


class AnimeThemeSong():
    def setName(self, name):
        self.name = name
    def setSinger(self, singer):
        self.singer = singer
    def setType(self, type):
        self.type = type
