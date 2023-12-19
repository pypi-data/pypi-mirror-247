from dataclasses import dataclass
from typing import Literal

@dataclass
class NaceCode:
    number: str
    description: str
    is_correted: bool = False
    correction_ranking: int | None = None


@dataclass
class Address:
    source: str
    street: str | None = None
    number: str | None = None
    city: str | None = None
    postal_code: str | None = None
    additionnal_address_info: str | None = None
    scraped_address: str | None = None
    last_update: str | None = None

@dataclass
class Email:
    source: str
    email: str

@dataclass
class Phone:
    source: str
    phone: str

@dataclass
class Website:
    source: str
    website: str

@dataclass
class BoardMember:
    is_company: bool
    function: str
    name: str
    start_date: str
    linked_company_number: str | None = None

@dataclass
class SocialNetwork:
    name: str
    url: str

@dataclass
class Establishment:
    establishment_number: str
    status: str | None = None
    start_date: str | None = None
    country: Literal["BE"] = "BE"
    name: str | None = None
    name_fr: str | None = None
    name_nl: str | None = None
    name_last_update: str | None = None
    social_networks: list[SocialNetwork] | None = None
    
    # These can have multiple values found on different sources
    # The best value is the one in best_address (re-computed on a regular basis)
    best_address: str | None = None
    addresses: list[Address] | None = None
    best_email: str | None = None
    emails: list[Email] | None = None
    best_phone: str | None = None
    phones: list[Phone] | None = None
    best_website: str | None = None
    websites: list[Website] | None = None
    
    end_date: str | None = None
    nace_codes: list[NaceCode] | None = None
    is_nace_codes_corrected: bool = False

@dataclass
class Company:
    # A combination of country ISO code and country_company_id in format: BE_1234567890
    inoopa_id: str
    # VAT number in Belgium for ex, SIRET in France,...
    company_number: str
    country: Literal["BE", "FR", "NL"] = "BE"
    legal_situation: str | None = None
    status: str | None = None
    start_date: str | None = None
    entity_type: str | None = None
    legal_form: str | None = None
    
    # These can have multiple values found on different sources
    # The best value is the one in best_address (re-computed on a regular basis)
    best_address: str | None = None
    addresses: list[Address] | None = None
    best_email: str | None = None
    emails: list[Email] | None = None
    best_phone: str | None = None
    phones: list[Phone] | None = None
    best_website: str | None = None
    websites: list[Website] | None = None
    
    name: str | None = None
    name_fr: str | None = None
    name_nl: str | None = None
    name_last_update: str | None = None
    social_networks: list[SocialNetwork] | None = None
    number_of_establishments: int | None = None
    establishments: list[Establishment] | None = None
    end_date: str | None = None
    legal_situation_last_update: str | None = None
    legal_form_last_update: str | None = None
    board_members: list[BoardMember] | None = None
    nace_codes: list[NaceCode] | None = None
    is_nace_codes_corrected: bool | None = False
    employee_category_code: int | None = None
    employee_category_formatted: str | None = None
