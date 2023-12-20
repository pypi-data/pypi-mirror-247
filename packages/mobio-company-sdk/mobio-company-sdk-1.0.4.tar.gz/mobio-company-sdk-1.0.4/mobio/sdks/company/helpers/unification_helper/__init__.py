from enum import Enum


class UnificationLogicalOperators:
    AND_OPERATOR = "and"
    OR_OPERATOR = "or"


class UnificationMatchRule:
    MATCH_TYPE = "match_type"
    NORMALIZED_TYPE = "normalized_type"
    MATCH_VALUE = "match_value"


class UnificationMatchType:
    EXACT = "exact"
    FUZZY = "fuzzy"
    EXACT_NORMALIZED = "exact_normalized"


class UnificationNormalizedType:
    PHONE_NUMBER = "phone"
    EMAIL = "email"
    UUID = "uuid"
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    OBJECT_ID = "object_id"


class UnificationStructure:
    # ROOT Structure
    RULE_ID = "id"
    SOURCE = "source"
    EDITABLE = "editable"
    DELETABLE = "deletable"
    DISABLE = "disable"
    STATUS = "status"
    SHOW = "show"

    # FILTER field
    UNIFICATION_VALUE = 'unification_value'

    # Nested Structure
    LOGICAL_OPERATORS = "logical_operators"
    OPERATORS = "operators"
    PRIORITY = "priority"
    FIELDS = "fields"
    UNIQUE = "unique"
    IS_DEFAULT = "is_default"

    DEFAULT_CONSENT = "consent"


class UnificationStatus:
    ENABLE = 1
    DISABLE = 0
    DELETED = -1


class UnificationDefaultDataSource:
    FILE = "Nhập Từ File"
    SINGLE = "Nhập Thủ Công"
    OTHER = "Other"
    SALE = "Sale"
    CORE = "CORE"


class UnificationSupportRule(Enum):
    ID = "id"
    NAME = "name"
    CIF = "cif"
    TAX_IDENTIFICATION_NUMBER = "tax_identification_number"
    PHONE_NUMBER = "phone_number"
    EMAIL = "email"
    SOURCE_COMPANY_ID = 'source_company_id'
    ALL_PHONE_NUMBER = 'all_phone_number'
    ALL_EMAIL = 'all_email'


