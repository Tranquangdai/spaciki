from itertools import groupby


def merge_matches(matches):
    """Merge overlapping pattern matches into an union match.

    Parameters
    ----------
    matches: list of dict
        Each dict contains 3 elements:
            {
                'label': <match_id>,
                'start': <start>,
                'end': <end>,
            }
        A match has a <match_id> which we can used to extract the phrase rule name.
        The <start> and <end> specify the begin and end character position of the match.

    Return
    ------
    new_matches: list of matches
        the new list of matches when merging overlapping matches
    """
    new_matches = list()
    matches = sorted(matches, key=lambda x: (x['label'], x['start'], x['end']))
    for group_name, group_elements in groupby(matches, key=lambda x: x['label']):
        group_elements = list(group_elements)
        i = 0
        j = i + 1
        max_r1 = group_elements[i]['end']
        while j < len(group_elements):
            left, right = group_elements[i], group_elements[j]
            l1, r1 = left['start'], left['end']
            l2, r2 = right['start'], right['end']
            if l1 <= l2 and l2 <= r1:
                max_r1 = max(r2, max_r1)
                j += 1
            else:
                left, right = group_elements[i], group_elements[j - 1]
                l1, r1 = left['start'], left['end']
                l2, r2 = right['start'], right['end']
                new_matches.append({'label': left['label'], 'start': l1, 'end': max_r1})
                i = j
                j = i + 1
                max_r1 = group_elements[i]['end']
        if len(group_elements) == 1:
            new_matches.append({'label': group_elements[i]['label'],
                                'start': group_elements[i]['start'],
                                'end': group_elements[i]['end']})
        else:
            left, right = group_elements[i], group_elements[j - 1]
            l1, r1 = left['start'], left['end']
            l2, r2 = right['start'], right['end']
            new_matches.append({'label': left['label'], 'start': l1, 'end': max_r1})
    return new_matches
