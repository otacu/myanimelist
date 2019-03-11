# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors


class MyanimelistPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', '123456', 'python', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if spider.name == 'anime':
            insert_anime_sql = """
                insert into tb_myanimelist_anime(en_name, jp_name, pic, `type`, episodes, premiered, producers, studios, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_anime_sql, (item["enName"], item["jpName"], item["pic"], item["type"], item["episodes"], item["premiered"], item["producers"], item["studios"], item["source"]))
            # 插入动画角色
            for character in item['characters']:
                insert_anime_character_sql = """
                        insert into tb_myanimelist_anime_character(anime_en_name, anime_jp_name, `name`, voice_actor)
                        VALUES (%s, %s, %s, %s)
                    """
                self.cursor.execute(insert_anime_character_sql, (item["enName"], item["jpName"], character.characterName, character.voiceActor))
            # 插入制作人员
            for staff in item['staffs']:
                insert_anime_staff_sql = """
                        insert into tb_myanimelist_anime_staff(anime_en_name, anime_jp_name, `name`, roles)
                        VALUES (%s, %s, %s, %s)
                    """
                self.cursor.execute(insert_anime_staff_sql, (item["enName"], item["jpName"], staff.name, staff.roles))
            # 插入主题曲
            for themeSong in item['themeSongs']:
                insert_anime_themesong_sql = """
                        insert into tb_myanimelist_anime_themesong(anime_en_name, anime_jp_name, `name`, singer, `type`)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                self.cursor.execute(insert_anime_themesong_sql, (item["enName"], item["jpName"], themeSong.name, themeSong.singer, themeSong.type))
            self.conn.commit()
