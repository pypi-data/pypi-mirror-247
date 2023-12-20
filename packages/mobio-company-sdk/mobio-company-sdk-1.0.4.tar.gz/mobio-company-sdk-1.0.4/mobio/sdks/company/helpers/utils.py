import re
import phonenumbers
from bson.objectid import ObjectId
import uuid
from bson.binary import Binary, UuidRepresentation
from .. import LOG_HEADER


def chuan_hoa_so_dien_thoai_v2(so_dien_thoai):
    if not so_dien_thoai:
        return None
    so_dien_thoai = chuan_hoa_so_dien_thoai_theo_dau_so_moi(so_dien_thoai)
    try:
        parse = phonenumbers.parse(so_dien_thoai, 'VN')
        if so_dien_thoai.startswith('+84') or so_dien_thoai.startswith('84'):
            is_valid = validate_phone(so_dien_thoai)
        else:
            is_valid = phonenumbers.is_valid_number(parse)
        result = phonenumbers.format_number(
            parse, phonenumbers.PhoneNumberFormat.E164)
    except Exception as e:
        print("chuan_hoa_so_dien_thoai_v2:: Exception: {},{} ".format(
            so_dien_thoai, str(e)))
        is_valid = False
        result = None
    if is_valid and 12 <= len(str(result)) <= 13:
        return result
    else:
        return None
    
def chuan_hoa_so_dien_thoai_theo_dau_so_moi(so_dien_thoai):
    so_dien_thoai = re.sub(
        r'^(0|\+84|84)12([068])', r'\g<1>7\g<2>', so_dien_thoai)
    so_dien_thoai = re.sub("^(0|\+84|84)121", "\g<1>79", so_dien_thoai)
    so_dien_thoai = re.sub("^(0|\+84|84)122", "\g<1>77", so_dien_thoai)
    so_dien_thoai = re.sub(
        "^(0|\+84|84)12([345])", "\g<1>8\g<2>", so_dien_thoai)
    so_dien_thoai = re.sub("^(0|\+84|84)127", "\g<1>81", so_dien_thoai)
    so_dien_thoai = re.sub("^(0|\+84|84)129", "\g<1>82", so_dien_thoai)
    so_dien_thoai = re.sub(
        "^(0|\+84|84)16([2-9])", "\g<1>3\g<2>", so_dien_thoai)
    so_dien_thoai = re.sub(
        "^(0|\+84|84)18([68])", "\g<1>5\g<2>", so_dien_thoai)
    so_dien_thoai = re.sub("^(0|\+84|84)199", "\g<1>59", so_dien_thoai)

    return so_dien_thoai

def validate_phone(phone_number):
    try:
        pattern_phone_number = "^(\+?84|0)?(1(2([0-9])|6([2-9])|88|86|99)|9([0-9]{1})|8([0-9]{1})|7[0|6-9]|3[2-9]|5[2|5|6|8|9])+([0-9]{7})$"
        valid = re.match(pattern_phone_number, phone_number)
    except Exception as ex:
        print(f'{LOG_HEADER}ERROR::utils::validate_phone: {ex}')
        valid = None
    return True if valid is not None else False

def validate_email(email):
    if not email:
        return False
    try:
        valid = re.match(
            "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)
    except Exception as ex:
        print(f'{LOG_HEADER}ERROR::utils::validate_email: {ex}')
        valid = None
    return True if valid is not None else False

def normalize_object_id(some_object_id):
    if isinstance(some_object_id, str):
        return ObjectId(some_object_id)
    elif isinstance(some_object_id, list):
        return [ObjectId(x) if isinstance(x, str) else x for x in some_object_id]
    return some_object_id

# def normalize_uuid(some_uuid):
#     if isinstance(some_uuid, str):
#         return uuid.UUID(some_uuid)
#     return some_uuid

def binary_to_string(val):
    if isinstance(val, Binary):
        int_data = int.from_bytes(val, byteorder='big')
        uuid_obj = uuid.UUID(int=int_data)
        uuid_str = str(uuid_obj)
        return uuid_str
    else:
        return val


def normalize_uuid(val):
    try:
        return Binary.from_uuid(uuid.UUID(str(val)), UuidRepresentation.PYTHON_LEGACY)
    except ValueError:
        return val