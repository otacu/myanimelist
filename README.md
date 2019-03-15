# myanimelist
myanimelist.net的动画信息抓取

代理ip池用的[jhao104/proxy_pool](https://github.com/jhao104/proxy_pool),注意抓取https的网站要[修改](https://github.com/jhao104/proxy_pool/issues/156)。

无效的ip会在请求抛错误时删除，剩下的可用代理ip太少，用同一ip做代理的概率变大，目标网站就会返回429请求频繁。

setting.py中有个LOAD_ANIME_ID_FROM_FILE参数，设置为True可以使用anime_id_config.txt指定的animeId发请求。