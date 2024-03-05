import re
from typing import List

from rest_api.schemas.item import ArticleItem


class PreProcessing:
    def __init__(self) -> None:
        self.remove_html_pattern = re.compile(
            r"<[^< A-Z].*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});", re.DOTALL
        )
        self.remove_escape_character_pattern = re.compile(r"([\r|\n|\t])+")
        self.separate_article_pattern = re.compile(
            r"(Điều \d+\..*?)(?=Điều \d+\.|$)", re.DOTALL
        )
        self.separate_title_content_article_pattern = re.compile(
            r"(^Điều \d+\..*?\r\n\r\n)(.*)", re.DOTALL
        )

    def extract_article(self, legal_text: str) -> List[str]:
        """extract articles inside of legal documents if it exists

        Args:
            legal_text (str): legal text

        Returns:
            List[str]: list of articles inside of legal documents if it exists
        """
        # extract the articles inside of legal document
        articles = re.findall(self.separate_article_pattern, legal_text)

        if articles:
            # extract content and title of articles
            articles = [
                self.extract_content_title_article(article) for article in articles
            ]

        return articles

    def extract_content_title_article(self, article: str) -> tuple:
        """Extract article to title and content if it exists

        Args:
            article (str): article

        Returns:
            tuple: (title, content) if it exists
        """
        return re.findall(self.separate_title_content_article_pattern, article)

    def __pre_process_text(self, legal_text: str) -> str:
        """Preprocessing text

        Args:
            legal_text (str): a legal document

        Returns:
            str: a legal document after preprocessing
        """
        legal_text = self.remove_html_tag(legal_text)

        return legal_text

    def __post_process_text(self, text: str) -> str:
        """Post processing text

        Args:
            text (str): any string

        Returns:
            str: string after post processing
        """
        text = self.remove_escape_character(text)
        text = text.strip()
        return text

    def process(self, legal_text: str) -> List[ArticleItem]:
        """Extract clean articles from legal text if it exists

        Args:
            legal_text (str): a legal document

        Returns:
            List[ArticleItem]: a list of articles inside a legal document if it exists
        """
        articles = []
        if legal_text:
            legal_text = self.__pre_process_text(legal_text)
            articles = self.extract_article(legal_text)
            articles = [
                (self.__post_process_text(title), self.__post_process_text(content))
                for (title, content) in articles
            ]
            articles = [
                ArticleItem(i, title, content)
                for i, (title, content) in enumerate(articles)
            ]

        return articles
    
    def remove_html_tag(self, text: str) -> str:
        """Remove html tags inside text if it exists

        Args:
            text (str): input text

        Returns:
            str: output string without html tags
        """
        return re.sub(self.remove_html_pattern, " ", text)

    def remove_escape_character(self, text: str) -> str:
        """Remove escape characters inside of text if it exists

        Args:
            text (str): text

        Returns:
            str: text without escape characters if it exists
        """
        return re.sub(self.remove_escape_character_pattern, text)
