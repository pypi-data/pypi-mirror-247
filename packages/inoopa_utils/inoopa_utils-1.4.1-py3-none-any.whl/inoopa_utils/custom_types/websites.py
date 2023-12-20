from dataclasses import dataclass


@dataclass
class PageInfo:
    url: str
    content: str | None = None

@dataclass
class CompanyWebsiteContent:
    url: str
    home: PageInfo| None = None
    about: PageInfo | None = None
    contact: PageInfo | None =  None
