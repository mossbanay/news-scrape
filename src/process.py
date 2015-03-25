from collections import Counter
import database

def get_all_detail_words():
    """Get all detail words
    
    Querys the database to fetch all details and process each detail to get all words. 
    This function does not remove duplicate words.

    Returns:
        List of all words used in all details.
    """
    headlines = database.query_all_headlines()

    words = set([])
    for headline in headlines:
        for word in headline['Detail'].lower().split():
            words.append(word)

    return words

def get_latest_detail_cloud_words(number_of_words=25):
    """Get all detail cloud words

    Gets all words used in details and counts the frequency of each word, before converting
    them into a format that can be used by d3-cloud with a javascript map function.

    Returns:
        List of lists in format of [word, frequency]
    """
    words = get_latest_detail_words()
    freqs = dict(Counter(words).most_common(number_of_words))
    result = []
    for word in freqs:
        result.append([word, freqs[word]])
    return result
