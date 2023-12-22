
from dataclasses import dataclass, field
from datetime import timedelta
import datetime
from mediawiki import MediaWiki as MW
from typing_extensions import TypedDict
from typing import Optional
import mediawiki as pymw
from zrcl3.mediawiki.parser import MediaWikiRawData

class MediaWikiConfig(TypedDict):
    lang: str  # Language of the MediaWiki site
    timeout: Optional[float]  # HTTP timeout setting; None for no timeout
    rate_limit: bool  # Use rate limiting or not
    rate_limit_wait: timedelta  # Time to wait between requests
    cat_prefix: str  # Prefix for categories used by the MediaWiki site
    user_agent: str  # User agent string for making requests
    username: Optional[str]  # Username for MediaWiki login
    password: Optional[str]  # Password for MediaWiki login
    proxies: Optional[str]  # Proxies for the Requests library

@dataclass
class MediaWiki:
    url : str
    mediaWikiSettings : MediaWikiConfig = field(default_factory=lambda: {"rate_limit" : True})
    expireDelta : timedelta = field(default_factory=lambda: timedelta(days=1))
    
    def __post_init__(self):
        self._pymw = MW(self.url, **self.mediaWikiSettings)
        self.__cached_pymw_pages = {}
        self.__cached_parsed_data = {}
        self.__last_fetched = {}
        self.__revisions = {}
    def __repr__(self):
        return f"MediaWiki({self.url})"
    
    def __update_revision(self, title : str):
        if title not in self.__last_fetched or self.__last_fetched[title] + self.expireDelta > datetime.datetime.now():
            return
        
        lastpaged = self.__cached_pymw_pages.pop(title)
        lastdata = self.__cached_parsed_data.pop(title, None)
        
        self.__last_fetched.pop(title)
        self.__revisions[(title, self.__last_fetched[title])] = (lastpaged, lastdata)

    def pagePyMw(self, title: str) -> pymw.MediaWikiPage:
        self.__update_revision(title)
        if title not in self.__cached_pymw_pages:
            self.__cached_pymw_pages[title] = self._pymw.page(title)
            self.__last_fetched[title] = datetime.datetime.now()
        
        return self.__cached_pymw_pages[title]
    
    def page(self, title: str):
        self.__update_revision(title)
        if title not in self.__cached_parsed_data:
            paged = self.pagePyMw(title)
            res = MediaWikiRawData(paged.content)
            self.__cached_parsed_data[title] = res
            self.__last_fetched[title] = datetime.datetime.now()
        return self.__cached_parsed_data[title]
    
    