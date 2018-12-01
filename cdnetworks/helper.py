def select_item_by_user(items, show_keys=True, *fields_to_show):
    selected_idx = 0
    if len(items) == 0:
        raise ValueError('No items found in List')
    if len(items) == 1:
        selected_idx = 1
    if len(items) > 1:
        for idx, actual_item in enumerate(items):
            string = ''
            if fields_to_show:
                for field in fields_to_show:
                    if field in actual_item:
                        string += str(field) + ' : ' if show_keys else ''
                        string += actual_item[field] + ', '
                string = string[:-1]
            else:
                string = actual_item
            print(idx + 1, ')', string)

        while True:
            try:
                session = int(input('Please make a selection (1-%d): ' % len(items)))
                if session > len(items) or session < 1:
                    raise ValueError
                selected_idx = session
                break
            except ValueError:
                print("'%s' is not a valid number." % session)

    return selected_idx - 1


def get_index_by_filter(items, expected_match, message):
    for idx, possible_match in enumerate(items):
        if expected_match in possible_match.values():
            return idx
    raise ValueError(message)


def select_from_list(items, expected_match, message="Value not found", *fields_to_show):
    """
        If Value set, get its dictonaty position.
        If not set ask user to select of list.
    """
    if expected_match:
        selected_idx = get_index_by_filter(items, expected_match, message)
    else:
        selected_idx = select_item_by_user(items, True, *fields_to_show)

    return items[selected_idx]
