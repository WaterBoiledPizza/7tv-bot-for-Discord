import requests
import json
from types import SimpleNamespace

f = open('config.json')
cfg = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

def searchemote(q):
    url = "https://7tv.io/v3/gql"
    query = {
                "variables": {
                    "query": q,
                    "limit": 10,
                    "page": 1,
                    "filter": {
                        "case_sensitive": cfg.case_sensitive,
                        "category": cfg.category,
                        "exact_match": cfg.exact_match,
                        "ignore_tags": cfg.ignore_tags,
                    },
                },
                "extensions": {},
                "operationName": 'SearchEmotes',
                "query": 'query SearchEmotes($query: String!, $page: Int, $limit: Int, $filter: EmoteSearchFilter) {\n  emotes(query: $query, page: $page, limit: $limit, filter: $filter) {\n    count\n    items {\n      id\n      name\n      listed\n      trending\n      owner {\n        id\n        username\n        display_name\n        tag_color\n        __typename\n      }\n      flags\n      images {\n        name\n        format\n        url\n        width\n        height\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}'
            }

    response = requests.post(url, json=query)
    info = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))#

    #print(json.dumps(info, indent=4))

    if info.data:
        return info.data.emotes.items
    else: return None

# def searchuser(q):
#     url = "https://7tv.io/v3/gql"
#     query = {
#                 "variables": {
#                     "query": q,
#                     "limit": 10,
#                     "page": 1,
#                     "filter": {
#                         "case_sensitive": cfg.search_settings.case_sensitive,
#                         "category": cfg.search_settings.category,
#                         "exact_match": cfg.search_settings.exact_match,
#                         "ignore_tags": cfg.search_settings.ignore_tags,
#                     },
#                 },
#                 "extensions": {},
#                 "operationName": 'SearchEmotes',
#                 "query": 'query SearchEmotes($query: String!, $page: Int, $limit: Int, $filter: EmoteSearchFilter) {\n  emotes(query: $query, page: $page, limit: $limit, filter: $filter) {\n    count\n    items {\n      id\n      name\n      listed\n      trending\n      owner {\n        id\n        username\n        display_name\n        tag_color\n        __typename\n      }\n      flags\n      images {\n        name\n        format\n        url\n        width\n        height\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}'
#             }
#
#     response = requests.post(url, json=query)
#     info = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
#
#     if info.data:
#         return info.data.emotes.items
#     else: return None


if __name__ == "__main__":
    searchemote("forsen")
    # print(searchemote("forsen"))