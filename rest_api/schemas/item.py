from datetime import date
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

        # Combine the field names and args to a dict
        # using the positions.
        kwargs = dict(zip(field_names, args))

        super().__init__(**kwargs)


class LawItem(BaseModel):
    lawId: int  # LawID
    newsCode: str  # News_Code
    subject: str  # News_Subject
    description: str  # SEO_Description
    newsDate: Optional[date | str]  # News_Date
    newsEffectDate: Optional[date | str]  # News_EffectDate
    newsEffectless: Optional[date | str]  # News_Effectless
    lawfields: List[LawFieldItem]
    lawOrganizationIds: Optional[List[int] | str]
    # lawStatus: LawStatusItem
    lawType: str
    content: str  # ContentVN

    def __init__(self, *args):
        # Get a "list" of field names (or key view)
        field_names = self.__fields__.keys()

        # Combine the field names and args to a dict
        # using the positions.
        kwargs = dict(zip(field_names, args))

        super().__init__(**kwargs)

    def convert_to_json(self) -> Dict:
        self.lawfields = [law_field.dict() for law_field in self.lawfields]

        return self.dict()


class LawQuestionAnswerPairItem(BaseModel):
    lawId: int
    question: str
    answerContent: str
    answerUrl: List

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
