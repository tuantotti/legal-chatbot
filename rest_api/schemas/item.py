from typing import Dict, List, Optional

from pydantic import BaseModel


class LawFieldItem(BaseModel):
    fieldId: int  # Field_ID
    lawFieldUrl: str  # LawFieldUrl
    fieldValue: int  # Field_Value
    fieldName: str  # Field_Name

    def __init__(self, *args):
        # Get a "list" of field names (or key view)
        field_names = self.__fields__.keys()

        # Combine the field names and args to a dict
        # using the positions.
        kwargs = dict(zip(field_names, args))

        super().__init__(**kwargs)


class LawOrganizationItem(BaseModel):
    orgId: int  # OrgID
    orgName: str  # OrgName
    priority: int  # UuTien
    entityState: int  # EntityState

    def __init__(self, *args):
        # Get a "list" of field names (or key view)
        field_names = self.__fields__.keys()

        # Combine the field names and args to a dict
        # using the positions.
        kwargs = dict(zip(field_names, args))

        super().__init__(**kwargs)


class LawStatusItem(BaseModel):
    statusId: int  # Status_ID
    statusName: str  # Status_Name
    entityState: int  # EntityState

    def __init__(self, *args):
        # Get a "list" of field names (or key view)
        field_names = self.__fields__.keys()
        print(self.model_fields)

        # Combine the field names and args to a dict
        # using the positions.
        kwargs = dict(zip(field_names, args))

        super().__init__(**kwargs)


class LawQuestionAnswerPairItem(BaseModel):
    lawId: int
    question: str
    answerContent: str
    answerUrl: str

    def __init__(self, *args):
        # Get a "list" of field names (or key view)
        field_names = self.__fields__.keys()

        # Combine the field names and args to a dict
        # using the positions.
        kwargs = dict(zip(field_names, args))

        super().__init__(**kwargs)


class ArticleItem(BaseModel):
    articleId: int
    title: str
    content: str

    def __init__(self, *args):
        # Get a "list" of field names (or key view)
        field_names = self.__fields__.keys()

        # Combine the field names and args to a dict
        # using the positions.
        kwargs = dict(zip(field_names, args))

        super().__init__(**kwargs)


class LawItem(BaseModel):
    lawId: int
    newsCode: Optional[str]  # News_Code
    articles: Optional[
        List[ArticleItem]
    ]  # this field will fill in preprocessing process
    content: Optional[str]

    def __init__(self, *args):
        # Get a "list" of field names (or key view)
        field_names = self.__fields__.keys()

        # Combine the field names and args to a dict
        # using the positions.
        kwargs = dict(zip(field_names, args))

        super().__init__(**kwargs)

    def convert_to_json(self) -> Dict:
        if self.articles:
            self.articles = [article.model_dump() for article in self.articles]

        return self.model_dump()
