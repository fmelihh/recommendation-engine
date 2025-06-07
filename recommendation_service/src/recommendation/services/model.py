import json
import requests
import numpy as np
import pandas as pd
from typing import Any
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationModel:
    def __init__(self):
        self._api_records = []
        self._comments_df = None
        self._restaurants_df = None

        # model = SentenceTransformer("intfloat/multilingual-e5-base")
        self.model = SentenceTransformer(
            "Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0", trust_remote_code=True
        )
        self.embeddings = None
        self._initialize_model_pipeline()

    def _enrich_comment(self, row: dict[str, Any]):
        restaurant_map = self._restaurants_df.set_index("restaurant_id").to_dict(
            orient="index"
        )
        restaurant = restaurant_map.get(row["restaurant_id"], {})
        return (
            f"passage: Comment: {row['comment']}. "
            f"Rating: {row['rating']}/5. "
            f"Restaurant: {restaurant.get('name', '')}, "
            f"City: {restaurant.get('city', '')}. "
            f"Restaurant Rating: {restaurant.get('rating', 'N/A')}/5."
        )

    def semantic_search(self, query: str, top_k=3):
        query_embedding = self.model.encode(
            f"query: {query}", normalize_embeddings=True
        )
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = []
        for i in top_indices:
            results.append(
                {
                    **self._comments_df.iloc[i].to_dict(),
                    "score": float(similarities[i]),
                }
            )
        return results

    def _initialize_model_pipeline(self):
        self._save_workflow_records()
        self._build_comments_df()
        self._build_restaurants_df()

        self._comments_df["enriched"] = self._comments_df.apply(
            self._enrich_comment, axis=1
        )

        self.embeddings = self.model.encode(
            self._comments_df["enriched"].tolist(), normalize_embeddings=True
        )

    def _build_comments_df(self):
        comment_list = []
        for element in self._api_records:
            if len(element["restaurant_comments"]) == 0:
                continue

            for comment in element["restaurant_comments"]:
                try:
                    if isinstance(comment, str):
                        comment = json.loads(
                            comment.replace('\\"', "").replace(
                                '"Yola çıktı"', '\\"Yola çıktı\\"'
                            )
                        )
                    comment_list.append(comment)
                except Exception as e:
                    print(e)
                    print(comment, type(comment))

        self._comments_df = pd.DataFrame(comment_list)

    def _build_restaurants_df(self):
        restaurant_list = []
        for element in self._api_records:
            del element["restaurant_comments"]
            del element["menu_items"]

            restaurant_list.append(element)

        self._restaurants_df = pd.DataFrame(restaurant_list)

    def _save_workflow_records(self):
        page = 1
        while 1:
            url = f"http://localhost:8000/recommendation_aggregate/recommendation-aggregate-data?page={page}&page_size=100"
            payload = {}
            headers = {"accept": "application/json"}

            response = requests.request("GET", url, headers=headers, data=payload)
            result = response.json()

            if len(result) == 0:
                break

            self._api_records.extend(result)
            page += 1


recommendation_model = None


def retrieve_recommendation_model() -> RecommendationModel:
    global recommendation_model
    if recommendation_model is None:
        recommendation_model = RecommendationModel()

    return recommendation_model


__all__ = ["recommendation_model", "retrieve_recommendation_model"]
