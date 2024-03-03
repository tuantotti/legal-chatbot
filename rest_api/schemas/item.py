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
    lawId: int  # LawID
    newsCode: str  # News_Code
    subject: str  # News_Subject
    description: str  # SEO_Description
    newsDate: Optional[str]  # News_Date
    newsEffectDate: Optional[str]  # News_EffectDate
    newsEffectless: Optional[str]  # News_Effectless
    lawfields: List[LawFieldItem]
    lawOrganizationIds: Optional[str]
    list_question_answer_pair: List[LawQuestionAnswerPairItem]
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
        self.lawfields = [law_field.model_dump() for law_field in self.lawfields]

        return self.model_dump()
