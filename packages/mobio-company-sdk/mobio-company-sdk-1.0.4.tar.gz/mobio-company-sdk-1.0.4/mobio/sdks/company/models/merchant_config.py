from .base_model import BaseModel


class CustomMerchantConfigStructure:
    _ID = '_id'
    MERCHANT_ID = 'merchant_id'
    CREATED_TIME = 'created_time'
    UPDATED_TIME = 'updated_time'

    DYNAMIC_FIELDS = 'dynamic_fields'
    PARENTS = 'parents'
    FIELD_TEMPLATE = 'field_template'
    TIMEZONE = 'timezone'
    VERSION = 'version'
    BASE_FIELDS = 'base_fields'
    INPUT = 'input'
    UPDATE = 'update'
    DYN_PS = 'dyn_ps'
    UNIFICATION_RULES = "unification_rules"


class MerchantConfig(BaseModel):
    def __init__(self):
        super().__init__()
        self.collection_name = 'merchant_config'
