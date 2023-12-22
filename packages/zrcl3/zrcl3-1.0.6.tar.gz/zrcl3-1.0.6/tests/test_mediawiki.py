from zrcl3.mediawiki import MediaWiki
from zrcl3.mediawiki.parser import MediaWikiRawData

def test_mediawiki_1():
    mw = MediaWiki(url="https://minecraft.fandom.com/api.php")
    res = mw._pymw.random(pages=1)
    fetched = mw.page(res)
    assert isinstance(fetched, MediaWikiRawData)
