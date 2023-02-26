import re

from django.shortcuts import redirect
from django.urls import re_path

from ..source import ProxySource
from ..source.data import ChapterAPI, SeriesAPI, SeriesPage
from ..source.helpers import api_cache, get_wrapper

from datetime import datetime

class Tachidesk(ProxySource):
    def get_reader_prefix(self):
        return "tachidesk"

    def shortcut_instantiator(self):
        def handler(request, album_hash):
            print("album_hash",album_hash)
            return redirect(
                f"reader-{self.get_reader_prefix()}-chapter-page",
                album_hash,
                "1",
                "1",
            )

        return [
            # We can't use /g/<hash> because nhentai uses that namespace already
            re_path(r"^tachidesk/(?P<album_hash>[\d\w]+)/$", handler),
        ]

    @staticmethod
    def image_url_handler(url):
        # This is likely unstable, but I haven't come across enough galleries to know
        # if all thumbnail -> original URLs map cleanly like so
        return re.sub(r"_\w.", "_o.", url.replace("thumbs2", "images2"))

    @api_cache(prefix="tachidesk_api_dt", time=0)
    def tachidesk_common(self, meta_id): # meta id sera talvez 192.168.1.172:4567/manga/1/
        meta_idTs = meta_id.replace("d",".").replace("p",":").replace("s","/")
        # print("metaid",meta_id,"metaidTs",meta_idTs)
        links = meta_idTs.split("/m")
        server= "http://"+links[0]
        api = "http://"+links[0]+"/api/v1/"
        manga = "m"+links[1]
        resp = get_wrapper(f"{api}{manga}")
        # print(resp.status_code,resp.json())
        if resp.status_code == 200:
            infos = resp.json()
            # test only
            getChapterInfo = get_wrapper(f"{api}{manga}chapters?onlineFetch=false")
            if getChapterInfo.status_code == 200:
                chapterData = getChapterInfo.json()
                # print(len(chapterData))
                chapter_list = []
                chapter_dict = {}
                for x in range(len(chapterData)):

                    atualIndex = chapterData[x]["index"]

                    test2 = [atualIndex, atualIndex, chapterData[x]["name"], atualIndex, chapterData[x]["scanlator"],datetime.utcfromtimestamp(int(chapterData[x]["fetchedAt"])),atualIndex]

                    chapterLink_list = []
                    for y in range(chapterData[x]["pageCount"]):
                        chapterLink_list.append(f"{api}{manga}chapter/{atualIndex}/page/{y}?useCache=false")

                    othersDict = {"volume": "1","title": chapterData[x]["name"]}
                    othersDict["groups"] = {"1": chapterLink_list}
                    chapter_dict[f"{atualIndex}"] = othersDict
                    chapter_list.append(test2)
                    # print(chapter_dict)\
                # print("testchapterAPi",chapter_dict["3"]["groups"]["1"])


            else:
                return None

            return {
                "slug": meta_id,
                "title": infos["title"],
                #"description": infos["description"],
                "description": infos["description"],
                "author": infos["author"],
                "artist": infos["artist"],
                "cover": f'{server}{infos["thumbnailUrl"]}',
                "groups": {"1": "test"},
                "chapter_dict": chapter_dict,
                "chapter_list": chapter_list,
                "original_url": f"http://{meta_idTs}",
            }
        else:
            return None

    @api_cache(prefix="tachidesk_series_dt", time=0)
    def series_api_handler(self, meta_id):
        data = self.tachidesk_common(meta_id)
        return (
            SeriesAPI(
                slug=data["slug"],
                title=data["title"],
                description=data["description"],
                author=data["author"],
                artist=data["artist"],
                groups=data["groups"],
                cover=data["cover"],
                chapters=data["chapter_dict"],
            )
            if data
            else None
        )

    @api_cache(prefix="tachidesk_pages_dt", time=0)
    def chapter_api_handler(self, meta_id):
        data = self.tachidesk_common(meta_id)
        return (
            ChapterAPI(
                pages=data["chapter_dict"]["1"]["groups"]["1"], series=data["slug"], chapter=data["slug"]
            )
            if data
            else None
        )

    @api_cache(prefix="tachidesk_series_page_dt", time=0)
    def series_page_handler(self, meta_id):
        data = self.tachidesk_common(meta_id)
        return (
            SeriesPage(
                series=data["title"],
                alt_titles=[],
                alt_titles_str=None,
                slug=data["slug"],
                cover_vol_url=data["cover"],
                metadata=[],
                synopsis=data["description"],
                author=data["author"],
                chapter_list=data["chapter_list"],
                original_url=data["original_url"],
            )
            if data
            else None
        )

