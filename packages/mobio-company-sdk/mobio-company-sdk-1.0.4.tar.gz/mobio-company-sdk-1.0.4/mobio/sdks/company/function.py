from . import LOG_HEADER
from .helpers.unification_helper.unified_company_by_source_helper import UnifiedCompanyBySource
from .models.merchant_config import MerchantConfig, CustomMerchantConfigStructure
from .models.company import CompanyStructure
from .helpers.utils import normalize_uuid


class MobioCompanySDK:
    def get_company_id(
            self, 
            merchant_id,
            company_data: dict,
        ):
        '''
        merchant_id: "" - Merchant id
        company_data: { - Thông tin công ty cần tìm
            "source": "", - Nguồn định danh công ty
            "...": "", - Các trường thông tin công ty
        }
        '''
        LOG_FUNCTION = f"{LOG_HEADER}MobioCompanySDK::get_company_id::"
        # Validate merchant_id
        try:
            if not merchant_id:
                mess = f"{LOG_HEADER} ERROR: merchant_id is not empty"
                raise Exception(mess)
            normalize_uuid(merchant_id)
        except Exception as ex:
            mess = f'{LOG_FUNCTION} ERROR: cannot convert merchant_id: {merchant_id} - ex: {ex}'
            raise Exception(mess)
        
        # Validate source
        source = company_data.get(CompanyStructure.SOURCE)
        if not source:
            mess = f"{LOG_HEADER} ERROR: source is not empty"
            raise Exception(mess)
        
        # Find merchant_config
        merchant_id = str(merchant_id)
        merchant_config = MerchantConfig().find_one(
            query={
                CustomMerchantConfigStructure.MERCHANT_ID: normalize_uuid(merchant_id)
            },
            fields=[CustomMerchantConfigStructure.UNIFICATION_RULES]
        )
        if not merchant_config:
            mess = f"{LOG_FUNCTION} ERROR: merchant_config not found"
            raise Exception(mess)
        
        # Find company
        unification_rules = merchant_config.get(CustomMerchantConfigStructure.UNIFICATION_RULES) or []
        company_satellite = UnifiedCompanyBySource().unified(
            merchant_id=merchant_id,
            source=source,
            company_data=company_data,
            all_rules=unification_rules,
        )
        if not company_satellite:
            return None
        company_id = company_satellite.get(CompanyStructure.ID)
        return company_id
