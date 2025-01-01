from pydantic import BaseModel, Field, field_validator


class SearchDto(BaseModel):
    page: int = Field(default=0)
    page_size: int = Field(default=10)
    search_text: str
    lat: str | None = Field(default=None)
    lon: str | None = Field(default=None)

    def generate_fuzzy_query_string(self, search_text: str | None = None) -> str:
        if search_text is None:
            search_text = self.search_text

        search_words = search_text.split(" ")
        search_words_with_tilde = []
        for word in search_words:
            word_length = len(word)
            tilde_num = 0
            if word_length >= 4:
                tilde_num = word_length // 4.0
                if tilde_num > 4:
                    tilde_num = 4

            if tilde_num > 0:
                word += f"~{int(tilde_num)}"
            search_words_with_tilde.append(word)
        return " ".join(search_words_with_tilde)

