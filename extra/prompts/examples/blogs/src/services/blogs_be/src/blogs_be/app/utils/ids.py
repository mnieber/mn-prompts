def insert_id(ids, parent_id, id):
    """Insert id into ids after parent_id, or at the end if
    parent_id is not found."""
    pos = ids.index(parent_id) + 1 if parent_id else len(ids)
    return ids[:pos] + [id] + ids[pos:]


def sort_items(items, keys, get_key):
    """Changes the values of `item.sort_pos` so that `items.map(get_key)`
    returns `keys`."""
    item_keys = [get_key(item) for item in items]
    valid_keys = [x for x in keys if x in item_keys]
    for item in items:
        new_sort_pos = valid_keys.index(get_key(item))
        assert new_sort_pos >= 0
        if new_sort_pos != item.sort_pos:
            item.sort_pos = new_sort_pos
            item.save()
