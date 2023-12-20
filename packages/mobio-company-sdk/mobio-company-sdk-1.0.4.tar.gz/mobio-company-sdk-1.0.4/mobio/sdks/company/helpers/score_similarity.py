from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import unicodedata
from .. import LOG_HEADER

class ScoreSimilarity:
    def temp(self, sentence):
        return len(sentence) == len(bytearray(sentence, "utf-8"))

    def vn2eng(self, str):
        str = re.sub("à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ", "a", str)
        str = re.sub("è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ", "e", str)
        str = re.sub("ì|í|ị|ỉ|ĩ", "i", str)
        str = re.sub("ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ", "o", str)
        str = re.sub("ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ", "u", str)
        str = re.sub("ỳ|ý|ỵ|ỷ|ỹ", "y", str)
        str = re.sub("đ", "d", str)
        str = re.sub("Đ", "D", str)

        str = re.sub("À|Á|Ạ|Ả|Ã|Â|Ầ|Ấ|Ậ|Ẩ|Ẫ|Ă|Ằ|Ắ|Ặ|Ẳ|Ẵ", "A", str)
        str = re.sub("È|É|Ẹ|Ẻ|Ẽ|Ê|Ề|Ế|Ệ|Ể|Ễ", "E", str)
        str = re.sub("Ì|Í|Ị|Ỉ|Ĩ", "I", str)
        str = re.sub("Ò|Ó|Ọ|Ỏ|Õ|Ô|Ồ|Ố|Ộ|Ổ|Ỗ|Ơ|Ờ|Ớ|Ợ|Ở|Ỡ", "O", str)
        str = re.sub("Ù|Ú|Ụ|Ủ|Ũ|Ư|Ừ|Ứ|Ự|Ử|Ữ", "U", str)
        str = re.sub("Ỳ|Ý|Ỵ|Ỷ|Ỹ", "Y", str)
        return str

    def score(self, name1, name2):
        try:
            name1_lower = unicodedata.normalize("NFC", name1).lower()
            name2_lower = unicodedata.normalize("NFC", name2).lower()
            vectorizer = TfidfVectorizer(
                use_idf=True, token_pattern="\S+", max_features=3000,
            )
            check_1 = self.temp(name1_lower)
            check_2 = self.temp(name2_lower)
            if check_1 and check_2:
                concat = [name1_lower, name2_lower]
                maxtrix_vec = vectorizer.fit_transform(
                    concat
                )  # Term Frequency-Inverse Document Frequency (TFIDF)
                vec_list = maxtrix_vec.toarray().tolist()
            else:
                concat = [self.vn2eng(name1_lower), self.vn2eng(name2_lower)]
                maxtrix_vec = vectorizer.fit_transform(
                    concat
                )  # Term Frequency-Inverse Document Frequency (TFIDF)
                vec_list = maxtrix_vec.toarray().tolist()
            s = cosine_similarity([vec_list[0]], [vec_list[1]])[0][0]
        except Exception as ex:
            print(f'{LOG_HEADER}ERROR::ScoreSimilarity::score: {ex}')
            s = 0
        return round(s, 2)


if __name__ == "__main__":
    print(ScoreSimilarity().score("Hoàng", "Hoàng"))
    print(ScoreSimilarity().score("Hoàng giang", "Giang Hoang"))
    print(ScoreSimilarity().score("Hoàng giang", "Giang Nguyen"))
    print(ScoreSimilarity().score("Hòa", "Hoà"))
