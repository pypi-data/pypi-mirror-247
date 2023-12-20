from pymongo import ReadPreference, WriteConcern
from .db_manager import DBManager

class BaseModel(object):
    db_name = None
    collection_name = None

    client_mongo = DBManager.get_instance().db

    def get_db(self, read_preference=None, write_concern=None):
        w = None
        if write_concern is not None:
            w = WriteConcern(w=write_concern)
        if not self.client_mongo:
            raise Exception('ERROR client_mongo: is {}'.format(self.client_mongo))
        return self.client_mongo.get_database(self.db_name)
    
    
    def collector(self):
        return self.get_db()[self.collection_name]

    def find_one(self, query, sort=None, fields=None):
        if fields is not None:
            fields_show = {"_id": 1}
            for field in fields:
                fields_show[field] = 1
        else:
            fields_show = None

        if sort:
            result = (
                self.collector().find_one(query, projection=fields_show, sort=sort)
            )
        else:
            result = (
                self.collector().find_one(query, projection=fields_show)
            )
        return result

    def find_all(
            self,
            query,
            per_page=None,
            sort=None,
            read_preference=ReadPreference.SECONDARY_PREFERRED,
    ):
        cursor = (
            self.collector().find(query)
        )
        if sort:
            cursor = cursor.sort(sort)
        if per_page:
            cursor = cursor.limit(limit=per_page)
        results = [x for x in cursor]
        return results
    
    def select_all(self, search_option, field_select=None):
        res = self.collector().find(search_option, field_select)
        return list(res)
