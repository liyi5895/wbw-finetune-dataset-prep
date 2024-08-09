import codecs

def clean_article_content(content):
    # Define a pattern that matches any of the given strings
    patterns = [
        "If you like Wait But Why, sign up for",
        "Related Wait But Why Posts",
        "If you liked this, these are for you too",
        "If you liked this post, check out",
        "What to read next:",
        "Tweet\n\t\t\t\t\t\t\t!function (d, s, id)"
    ]

    # Convert article to lower case for case-insensitive search
    content_lower = content.lower()
    
    # Initialize the end_index to the length of the article
    end_index = len(content)
    
    # Loop through each pattern and find the earliest occurrence
    for pattern in patterns:
        pattern_index = content_lower.find(pattern.lower())
        if pattern_index != -1:
            # Update end_index to the earliest found pattern index
            end_index = min(end_index, pattern_index)
    
    # Slice the article up to the earliest pattern index
    content = content[:end_index]
    
    return content