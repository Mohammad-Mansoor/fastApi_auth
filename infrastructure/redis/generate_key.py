import hashlib
import json


def generate_cache_key(namespace: str, base_key: str, query: dict = None):
    """
    Creates stable Redis key (same as NestJS version)

    Example:
    auth:roles:list:3f8ac1b9d2
    """

    query = query or {}

    lang = query.get("lang", "en")

    # remove lang if you want language-neutral caching
    query.pop("lang", None)

    # sort query for consistency
    sorted_query = json.dumps(query, sort_keys=True)

    # hash query
    hash_value = hashlib.md5(sorted_query.encode()).hexdigest()[:10]

    # final key
    return f"{namespace}:{base_key}:{hash_value}"