# -*- coding: utf-8 -*-
import scrapy
import re

from myanimelist.items import AnimeItem

url_prefix = "https://myanimelist.net/anime/{}"


class AnimeSpider(scrapy.Spider):
    name = 'anime'
    allowed_domains = ['myanimelist.net']
    # start_urls = [url_prefix.format(i) for i in range(35790, 35791)]
    # start_urls = [url_prefix.format(i) for i in range(1, 40000)]
    start_urls = [url_prefix.format(i) for i in range(90, 91)]

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
        # 角色和声优
        characterSel = sel.xpath('td[2]/div[1]/table/tr[2]/td[1]/div[1]')
        characters = []
        try:
            leftTableCharacterList = characterSel.xpath('div[1]/table/tr/td[2]/a/text()').extract()
            for index in range(len(leftTableCharacterList)):
                animeCharacter = AnimeCharacter()
                characterName = leftTableCharacterList[index]
                animeCharacter.setCharacterName(characterName)
                try:
                    indexStr = bytes(index + 1)
                    voiceActor = characterSel.xpath('div[1]/table['+indexStr+']/tr/td[3]/table/tr/td[1]/a/text()').extract()
                    animeCharacter.setVoiceActor(''.join(voiceActor))
                except:
                    pass
                characters.append(animeCharacter)
        except:
            pass
        try:
            rightTableCharacterList = characterSel.xpath('div[2]/table/tr/td[2]/a/text()').extract()
            for index in range(len(rightTableCharacterList)):
                animeCharacter = AnimeCharacter()
                characterName = rightTableCharacterList[index]
                animeCharacter.setCharacterName(characterName)
                try:
                    indexStr = bytes(index + 1)
                    voiceActor = characterSel.xpath('div[2]/table['+indexStr+']/tr/td[3]/table/tr/td[1]/a/text()').extract()
                    animeCharacter.setVoiceActor(''.join(voiceActor))
                except:
                    pass
                characters.append(animeCharacter)
        except:
            pass
        item['characters'] = characters
        # 制作人员
        staffSel = sel.xpath('td[2]/div[1]/table/tr[2]/td[1]/div[2]')
        staffs = []
        try:
            leftTableStaffList = staffSel.xpath('div[1]/table/tr/td[2]/a/text()').extract()
            for index in range(len(leftTableStaffList)):
                animeStaff = AnimeStaff()
                staffName = leftTableStaffList[index]
                animeStaff.setName(staffName)
                try:
                    indexStr = bytes(index + 1)
                    role = staffSel.xpath('div[1]/table['+indexStr+']/tr/td[2]/div/small/text()').extract()
                    animeStaff.setRoles(''.join(role))
                except:
                    pass
                staffs.append(animeStaff)
        except:
            pass
        try:
            rightTableStaffList = staffSel.xpath('div[2]/table/tr/td[2]/a/text()').extract()
            for index in range(len(rightTableStaffList)):
                animeStaff = AnimeStaff()
                staffName = rightTableStaffList[index]
                animeStaff.setName(staffName)
                try:
                    indexStr = bytes(index + 1)
                    role = staffSel.xpath('div[2]/table['+indexStr+']/tr/td[2]/div/small/text()').extract()
                    animeStaff.setRoles(''.join(role))
                except:
                    pass
                staffs.append(animeStaff)
        except:
            pass
        item['staffs'] = staffs
        # 主题曲
        themeSongSel = sel.xpath('td[2]/div[1]/table/tr[2]/td[1]/div[3]')
        themeSongs = []
        try:
            openingThemeDetailList = themeSongSel.xpath('div[1]/div/span/text()').extract()
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

        print(item)
        yield item


class AnimeCharacter():
    def setCharacterName(self, characterName):
        self.characterName = characterName
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
