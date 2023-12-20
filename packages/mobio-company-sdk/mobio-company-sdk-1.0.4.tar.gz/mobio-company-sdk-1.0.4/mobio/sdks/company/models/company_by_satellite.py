from .company import CompanyStructure
from ..helpers.unification_helper import (
    UnificationStructure,
    UnificationSupportRule,
)
from .base_model import BaseModel


class CompanyBySatellite(BaseModel):
    def __init__(self, merchant_id):
        super().__init__()
        self.collection_name = "company_by_satellite_" + \
            str(merchant_id).lower()
        self.merchant_id = str(merchant_id)

    @staticmethod
    def create_unifies_value(field_name, value):
        prefix_unifies = "::_pu"
        return "{}::{}::{}".format(
            prefix_unifies,
            field_name,
            str(value),
        )

    def get_company_ids_by_cif(self, data, limit=None, count=False):
        field_key = UnificationSupportRule.CIF.value
        filter_value = []
        if type(data) == list:
            for value in data:
                if value is not None:
                    filter_value.append(
                        self.create_unifies_value(
                            field_name=field_key, value=value)
                    )
        else:
            if data:
                filter_value.append(
                    self.create_unifies_value(field_name=field_key, value=data)
                )
        if not filter_value:
            return None
        if not count:
            return self.get_company_ids_by_unification_values(
                values=filter_value, limit=limit
            )
        else:
            return self.count_company_by_unification_values(values=filter_value)

    def get_company_ids_by_tax_identification_number(self, data, limit=None, count=False):
        field_key = UnificationSupportRule.TAX_IDENTIFICATION_NUMBER.value
        filter_value = []
        if type(data) == list:
            for value in data:
                if value is not None:
                    filter_value.append(
                        self.create_unifies_value(
                            field_name=field_key, value=value)
                    )
        else:
            if data:
                filter_value.append(
                    self.create_unifies_value(field_name=field_key, value=data)
                )
        if not filter_value:
            return None
        if not count:
            return self.get_company_ids_by_unification_values(
                values=filter_value, limit=limit
            )
        else:
            return self.count_company_by_unification_values(values=filter_value)

    def get_company_ids_by_unification_values(self, values, limit=1000):
        if not values:
            return []
        if limit is None:
            limit = 1000
        result = (
            self.collector()
            .find({UnificationStructure.UNIFICATION_VALUE: {"$in": values}}, {CompanyStructure.ID: 1})
            .limit(limit)
        )
        return [x for x in result]
    
    def count_company_by_unification_values(self, values):
        if not values:
            return []
        result = self.get_db().count(
            {UnificationStructure.UNIFICATION_VALUE: {"$in": values}}
        )
        return result
    