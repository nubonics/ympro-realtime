def get_attr(obj, key, default=None):
    # Try dict-style first, then attribute
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)