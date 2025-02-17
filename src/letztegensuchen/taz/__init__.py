from bs4 import BeautifulSoup, SoupStrainer


class PageScraper(BeautifulSoup):
    def __init__(
        self,
        markup="",
        parse_only=SoupStrainer(["meta", "article"]),
        **kwargs,
    ):
        super().__init__(
            markup,
            features="html.parser",
            parse_only=parse_only,
            **kwargs,
        )
        self.article = {}
        self.article["id"], self.article["headline"] = self._get_article_id_headline()
        self.article["description"] = self._get_article_description()
        self.article["date_published"] = self._get_article_dt()
        self.article["authors"] = self._get_article_authors()
        self.article["tags"] = self._get_article_tags()
        self.article["text"] = self._get_article_text()

    def _get_article_id_headline(self) -> tuple[str, str]:
        meta = self.find("meta", attrs={"name": "taz:title"})
        if not meta:
            return None
        return meta["data-id"], meta["content"]

    def _get_article_description(self) -> str:
        meta = self.find("meta", attrs={"name": "description"})
        if not meta:
            return None
        return meta["content"]

    def _get_article_dt(self) -> str:
        meta = self.find("meta", attrs={"property": "article:published_time"})
        if not meta:
            return None
        return meta["content"]

    def _get_article_authors(self) -> str:
        meta_set = self.find_all("meta", attrs={"property": "article:author"})
        return [meta["content"] for meta in meta_set]

    def _get_article_tags(self) -> list[dict[str, str]]:
        meta_set = self.find_all("meta", attrs={"property": "article:tag"})
        return [
            {"id": meta["data-tag-id"], "name": meta["content"]} for meta in meta_set
        ]

    def _get_article_text(self) -> str:
        page_text = []
        if article_body := self.find(attrs={"class": "main-article-corpus"}):
            article_tags = article_body.select(".headline, p.typo-bodytext")
            for tag in article_tags:
                if text := tag.get_text():
                    page_text.append(text)
        return "\n\n".join(page_text)
    
    def to_string(self) -> str:
        text = []
        for key in ["id", "headline", "description", "text"]:
            if value := self.article[key]:
                text.append(value)
        return "\n\n".join(text)
