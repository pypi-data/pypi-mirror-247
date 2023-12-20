from operator import itemgetter
import uuid
from datetime import datetime, timedelta
from ..utils import chuan_hoa_so_dien_thoai_v2, validate_email, normalize_object_id
from ..score_similarity import ScoreSimilarity
from . import (
    UnificationSupportRule,
    UnificationMatchType,
    UnificationMatchRule,
    UnificationStructure,
    UnificationNormalizedType,
)
from ...models.company_by_satellite import CompanyBySatellite
from ...models.merchant_config import MerchantConfig
from ...models.company import CompanyStructure, Company
from ... import LOG_HEADER


class UnifiedCompanyBySource:
    def build_query(self, rule_operator, company_data, set_field_encrypt, merchant_id):
        priority = rule_operator.get(UnificationStructure.PRIORITY, 1)
        match_all_rule = []
        rule_other = set()
        normalized_by_source = dict()
        or_operator = []
        for k, v in rule_operator.get(UnificationStructure.FIELDS).items():
            instance_value = company_data.get(k)

            if instance_value:
                matched_rule = False
                normalized_type = v.get(UnificationMatchRule.NORMALIZED_TYPE)
                normalized_value = []
                match_type = v.get(UnificationMatchRule.MATCH_TYPE)
                if match_type in [
                    UnificationMatchType.EXACT_NORMALIZED,
                    UnificationMatchType.EXACT,
                ]:
                    if normalized_type == UnificationNormalizedType.PHONE_NUMBER:
                        lst_phone_valid = []
                        instance_value = instance_value if type(
                            instance_value) == list else [instance_value]
                        for phone in instance_value:
                            valid_phone = chuan_hoa_so_dien_thoai_v2(phone)
                            if valid_phone:
                                lst_phone_valid.append(valid_phone)
                                matched_rule = True
                        if lst_phone_valid:
                            for phone_valid in lst_phone_valid:
                                normalized_value.append(
                                    CompanyBySatellite.create_unifies_value(
                                        field_name=k,
                                        value=phone_valid,
                                    )
                                )

                    elif normalized_type == UnificationNormalizedType.EMAIL:
                        if type(instance_value) == list:
                            for email in instance_value:
                                email = str(email).lower().strip()
                                if validate_email(email):
                                    normalized_value.append(
                                        CompanyBySatellite.create_unifies_value(
                                            field_name=k,
                                            value=email,
                                        )
                                    )
                                    matched_rule = True
                        else:
                            email = str(instance_value).lower().strip()
                            if validate_email(email):
                                normalized_value.append(
                                    CompanyBySatellite.create_unifies_value(
                                        field_name=k,
                                        value=email,
                                    )
                                )
                                matched_rule = True
                    elif normalized_type in [
                        UnificationNormalizedType.UUID,
                        UnificationNormalizedType.INT,
                        UnificationNormalizedType.FLOAT,
                        UnificationNormalizedType.STRING,
                    ]:
                        try:
                            if type(instance_value) == list:
                                for single_instance_value in instance_value:
                                    single_instance_value = (
                                        uuid.UUID(single_instance_value)
                                        if normalized_type
                                        == UnificationNormalizedType.UUID
                                        else int(single_instance_value)
                                        if normalized_type
                                        == UnificationNormalizedType.INT
                                        else float(single_instance_value)
                                        if normalized_type
                                        == UnificationNormalizedType.FLOAT
                                        else str(single_instance_value)
                                    )
                                    normalized_value.append(
                                        CompanyBySatellite.create_unifies_value(
                                            field_name=k,
                                            value=single_instance_value,
                                        )
                                    )
                                    matched_rule = True
                            else:
                                value = (
                                    uuid.UUID(instance_value)
                                    if normalized_type
                                    == UnificationNormalizedType.UUID
                                    else int(instance_value)
                                    if normalized_type
                                    == UnificationNormalizedType.INT
                                    else float(instance_value)
                                    if normalized_type
                                    == UnificationNormalizedType.FLOAT
                                    else str(instance_value)
                                )
                                normalized_value.append(
                                    CompanyBySatellite.create_unifies_value(
                                        field_name=k,
                                        value=value,
                                    )
                                )
                                matched_rule = True
                        except Exception as ex:
                            mess = '{}ERROR::UnifiedCompanyBySource::build_query: instance_value: {} err: {}'.format(
                                LOG_HEADER,
                                instance_value,
                                ex
                            )
                            print(mess)
                            matched_rule = False
                    else:
                        mess = f'normalized_type: {normalized_type} is not support'
                        raise Exception(mess)

                    if normalized_value:
                        normalized_by_source[k] = {
                            UnificationMatchRule.MATCH_TYPE: match_type,
                            UnificationMatchRule.MATCH_VALUE: normalized_value,
                            UnificationStructure.PRIORITY: priority,
                        }
                        rule_other.update(normalized_value)
                        
                elif match_type in [UnificationMatchType.FUZZY]:
                    normalized_by_source[k] = {
                        UnificationMatchRule.MATCH_TYPE: match_type,
                        UnificationMatchRule.MATCH_VALUE: [
                            str(x) for x in instance_value
                        ]
                        if type(instance_value) == list
                        else str(instance_value),
                        UnificationStructure.PRIORITY: priority,
                    }
                    matched_rule = True
                match_all_rule.append(matched_rule)
            else:
                match_all_rule.append(False)
                break
        if all(match_all_rule):
            if rule_other:
                result = [list(rule_other)]
            else:
                result = []
            for query_value in result:
                if query_value:
                    or_operator.append(
                        {UnificationStructure.UNIFICATION_VALUE: {"$all": query_value}}
                    )
        return or_operator, normalized_by_source

    def get_rule_by_source(self, all_rules, source):
        rule = next(
            (
                x
                for x in all_rules
                if x.get(UnificationStructure.SOURCE).lower() == str(source).lower()
            ),
            None,
        )
        if not rule:
            rule = next(
                (x for x in all_rules if x.get(UnificationStructure.IS_DEFAULT)),
                None,
            )
        return rule

    def find_by_source(
        self,
        merchant_id: str,
        source: str,
        company_data: dict,
        all_rules: list,
        is_inserted=False,
        set_field_encrypt=None
    ):
        or_operator = []
        lst_normalized = []
        field_get_data = {
            CompanyStructure.ID: 1
        }
        if CompanyStructure._ID in company_data or CompanyStructure.ID in company_data:
            try:
                company_id = company_data.get(CompanyStructure._ID)
                normalize_object_id(company_id)
            except Exception as ex:
                print(f"{LOG_HEADER}UnifiedCompanyBySource::find_by_source: ERROR: {ex}")
                company_id = None
            if company_id:
                or_operator.append(
                    {
                        UnificationStructure.UNIFICATION_VALUE: {
                            "$all": [
                                CompanyBySatellite.create_unifies_value(
                                    field_name=CompanyStructure.ID,
                                    value=company_id,
                                )
                            ]
                        }
                    }
                )
                lst_normalized.append(
                    {
                        CompanyStructure.ID: {
                            UnificationMatchRule.MATCH_TYPE: UnificationMatchType.EXACT,
                            UnificationMatchRule.MATCH_VALUE: [
                                CompanyBySatellite.create_unifies_value(
                                    field_name=CompanyStructure.ID,
                                    value=company_id,
                                )
                            ],
                            UnificationStructure.PRIORITY: 0,
                        }
                    }
                )

        rule = self.get_rule_by_source(all_rules=all_rules, source=source)
        if not rule:
            mess = f'{LOG_HEADER}UnifiedCompanyBySource::source: {source} is not exists'
            raise Exception(mess)
        
        for rule_operator in rule.get(UnificationStructure.OPERATORS):
            nested_or_operator, nested_normalized_by_source = self.build_query(
                rule_operator=rule_operator, company_data=company_data, set_field_encrypt=set_field_encrypt, merchant_id=merchant_id)
            if nested_or_operator:
                or_operator.extend(nested_or_operator)
                lst_normalized.append(nested_normalized_by_source)
                field_get_data.update(
                    {x: 1 for x in nested_normalized_by_source.keys()})
        if not or_operator:
            mess = f'{LOG_HEADER}UnifiedCompanyBySource::query: has no operator'
            raise Exception(mess)
        
        query = {"$or": or_operator}

        result = CompanyBySatellite(merchant_id=merchant_id).collector().find(
            query, field_get_data).limit(1000)
        result = list(result)
        tmp_lst_company = []

        for company in result:
            for normalized_by_source in lst_normalized:
                lst_matched = []
                priority = 0
                for k, v in normalized_by_source.items():
                    priority = v.get(UnificationStructure.PRIORITY, 1)
                    instance_value = company.get(k)
                    matched = False
                    if instance_value is not None:
                        if type(instance_value) == list:
                            for i_v in instance_value:
                                if v.get(UnificationMatchRule.MATCH_TYPE) in [
                                    UnificationMatchType.EXACT_NORMALIZED,
                                    UnificationMatchType.EXACT,
                                ]:
                                    match_value = v.get(
                                        UnificationMatchRule.MATCH_VALUE
                                    )
                                    if type(match_value) == list:
                                        for m_v in match_value:
                                            if str(
                                                CompanyBySatellite.create_unifies_value(
                                                    field_name=k,
                                                    value=i_v,
                                                )
                                            ) == str(m_v):
                                                matched = True
                                                break
                                    else:
                                        if str(match_value) == str(
                                            CompanyBySatellite.create_unifies_value(
                                                field_name=k,
                                                value=i_v,
                                            )
                                        ):
                                            matched = True
                                            break
                                else:
                                    score = ScoreSimilarity().score(
                                        str(v.get(UnificationMatchRule.MATCH_VALUE)),
                                        str(i_v),
                                    )
                                    if score >= 0.8:
                                        matched = True
                                        break
                        else:
                            if v.get(UnificationMatchRule.MATCH_TYPE) in [
                                UnificationMatchType.EXACT_NORMALIZED,
                                UnificationMatchType.EXACT,
                            ]:
                                match_value = v.get(
                                    UnificationMatchRule.MATCH_VALUE)
                                if type(match_value) == list:
                                    for m_v in match_value:
                                        if str(
                                            CompanyBySatellite.create_unifies_value(
                                                field_name=k,
                                                value=instance_value,
                                            )
                                        ) == str(m_v):
                                            matched = True
                                            break
                                else:
                                    if str(match_value) == str(
                                        CompanyBySatellite.create_unifies_value(
                                            field_name=k,
                                            value=instance_value,
                                        )
                                    ):
                                        matched = True
                            else:
                                score = ScoreSimilarity().score(
                                    str(v.get(UnificationMatchRule.MATCH_VALUE)),
                                    str(instance_value),
                                )
                                if score >= 0.8:
                                    matched = True
                    lst_matched.append(matched)
                if len(lst_matched) > 0 and all(lst_matched):
                    tmp_lst_company.append({"p": priority, "d": company})
                    break
        return tmp_lst_company

    def unified(
        self,
        merchant_id: str,
        source: str,
        company_data: dict,
        all_rules: list,
        is_inserted=False,
        set_field_encrypt=None
    ):
        tmp_lst_company = self.find_by_source(
            merchant_id=merchant_id,
            source=source,
            company_data=company_data,
            all_rules=all_rules,
            is_inserted=is_inserted,
            set_field_encrypt=set_field_encrypt
        )
        if tmp_lst_company:
            lst_company = sorted(tmp_lst_company, key=itemgetter("p"))
            max_priority = lst_company[0].get("p")
            # Lấy danh sách company có cùng priority
            lst_company = [
                x.get("d") for x in lst_company if x.get("p") == max_priority
            ]
        else:
            lst_company = []
        if not lst_company:
            return None
        if len(lst_company) > 1:
            unified_result = self.__compare_unified_company__(
                merchant_id=merchant_id, lst_company=lst_company
            )
            if not unified_result:
                return None
            else:
                return next(
                    (
                        x
                        for x in lst_company
                        if str(x.get(CompanyStructure.ID))
                        == str(unified_result)
                    ),
                    None,
                )
        else:
            return lst_company[0]

    def unified_by_data(self, merchant_id: str, datatype: str, data_value: list, set_field_encrypt=None):
        lst_company = None
        # if datatype in [
        #     UnificationSupportRule.PHONE_NUMBER.value,
        #     UnificationSupportRule.PRIMARY_PHONE.value,
        # ]:
        #     filter_values = list(data_value) if isinstance(
        #         data_value, Iterable) else [data_value]
        #     lst_valid_phone = []
        #     for filter_value in filter_values:
        #         valid_phone = chuan_hoa_so_dien_thoai_v2(filter_value)
        #         if valid_phone:
        #             lst_valid_phone.append(valid_phone)
        #     if set_field_encrypt and set_field_encrypt.get(datatype):
        #         encrypt_setting = set_field_encrypt.get(datatype)
        #         if str(encrypt_setting.get(AdminEncryptStructure.ENC_LEVEL)) == ModuleEncryptLevel.ENC_DB:
        #             # Vì lý do nghiệp vụ (VDS) nên cần extend thêm các sdt ko có PLUS sign vào list
        #             lst_valid_phone = lst_valid_phone + \
        #                 [str(x).replace("+", "") for x in lst_valid_phone]
        #         instance = dynamic_import_merge_v2(datatype)
        #         lst_valid_phone = instance.encrypt_value(
        #             merchant_id=merchant_id, data=lst_valid_phone, encrypt_setting=encrypt_setting)
        #     lst_company = CompanyBySatellite(
        #         merchant_id=merchant_id
        #     ).get_company_ids_by_phone(data=lst_valid_phone)
        # elif datatype in [
        #     UnificationSupportRule.EMAIL.value,
        #     UnificationSupportRule.PRIMARY_EMAIL.value,
        # ]:
        #     filter_values = list(data_value) if isinstance(
        #         data_value, Iterable) else [data_value]
        #     lst_valid_email = []
        #     for filter_value in filter_values:
        #         filter_value = str(filter_value).lower().strip()
        #         if validate_email(filter_value):
        #             lst_valid_email.append(filter_value)
        #     lst_company = CompanyBySatellite(
        #         merchant_id=merchant_id
        #     ).get_company_ids_by_email(data=lst_valid_email)
        if datatype == UnificationSupportRule.CIF.value:
            lst_company = CompanyBySatellite(
                merchant_id=merchant_id
            ).get_company_ids_by_cif(data=data_value)
        elif datatype == UnificationSupportRule.TAX_IDENTIFICATION_NUMBER.value:
            lst_company = CompanyBySatellite(
                merchant_id=merchant_id
            ).get_company_ids_by_tax_identification_number(data=data_value)
        # elif datatype == UnificationSupportRule.CUSTOMER_ID.value:
        #     lst_company = CompanyBySatellite(
        #         merchant_id=merchant_id
        #     ).get_company_ids_by_customer_id(data=data_value)
        # elif datatype == UnificationSupportRule.DEVICE_ID.value:
        #     lst_company = CompanyBySatellite(
        #         merchant_id=merchant_id
        #     ).get_company_ids_by_device(data=data_value)
        # elif datatype == UnificationSupportRule.SOCIAL_USER.value:
        #     lst_company = CompanyBySatellite(
        #         merchant_id=merchant_id
        #     ).get_company_ids_by_social_id(data=data_value)
        # elif datatype == UnificationSupportRule.COMPANY_IDENTIFY.value:
        #     lst_company = CompanyBySatellite(
        #         merchant_id=merchant_id
        #     ).get_company_ids_by_company_identify(data=data_value)
        # elif datatype == UnificationSupportRule.INTERNAL_ID.value:
        #     lst_company = CompanyBySatellite(
        #         merchant_id=merchant_id
        #     ).get_company_ids_by_internal_id(data=data_value)
        if not lst_company:
            return None
        if len(lst_company) > 1:
            unified_result = self.__compare_unified_company__(
                merchant_id=merchant_id, lst_company=lst_company
            )
            if not unified_result:
                return None
            else:
                return next(
                    (
                        x
                        for x in lst_company
                        if str(x.get(CompanyStructure.ID))
                        == str(unified_result)
                    ),
                    None,
                )
        else:
            return lst_company[0]

    @staticmethod
    def __compare_unified_company__(merchant_id, lst_company):
        """
        Describe:
        PRIORITY 1: Lấy theo company created_time đầu tiên
        :param merchant_id: id của merchant đang thực hiện
        :param lst_company: danh sách company cần tính toán limit 1000 đã lấy từ trước đó
        :param months: số tháng cần tính
        :return: Company Matched
        """
        results = []
        lst_company_raw = Company().select_all(
            search_option={
                CompanyStructure.MERCHANT_ID: str(merchant_id),
                CompanyStructure._ID: {
                    '$in': normalize_object_id([c.get(CompanyStructure.ID) for c in lst_company])
                }
            },
            field_select={
                CompanyStructure.MERCHANT_ID: 1,
                CompanyStructure._ID: 1,
                CompanyStructure.CREATED_TIME: 1,
            }
        )
        for company_data in lst_company_raw:
            results.append({
                "company_id": str(company_data.get(CompanyStructure._ID)),
                "created_time": -company_data.get(
                    CompanyStructure.CREATED_TIME
                ).timestamp(),
            })
        if results:
            results = sorted(
                results,
                key=itemgetter("created_time"),
                reverse=True,
            )
        return results[0].get("company_id") if results else None


if __name__ == '__main__':
    merchant_id = '1b99bdcf-d582-4f49-9715-1b61dfff3924'
    merchant_config = MerchantConfig().find_one({
        'merchant_id': uuid.UUID(merchant_id)
    })
    all_rules = merchant_config.get('unification_rules')
    result = UnifiedCompanyBySource().unified(
        merchant_id=merchant_id,
        source='MST',
        company_data={
            'tax_identification_number': '2342143322',
            'name': 'test tuan 1',
            'cif': '12345',
        },
        all_rules=all_rules,
        is_inserted=False,
        set_field_encrypt=None
    )
    print(result)
