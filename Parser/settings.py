# This is the settings for parse.py


# Headers for the CSV file
headers = [
        "Reviewer Name",  # reviewerName
        "Review content",  # reviewContent
        "Full review link",  # fullReviewLink
        "Rating",  # rating
        "Review Time Information",  # reviewTimeInformation
        "Did the shop owner reply",  # didOwnerReply
        "Reply text from Owner",  # replyTextFromOwner
    ]

# The index of the reviews in the JSON response
reviews_index = 2

# The format of the review data, must match the headers order
review_format = {
    "reviewerName": [0, 1],
    "reviewContent": [3],
    "fullReviewLink": [18],
    "rating": [4],
    "reviewTimeInformation": [1],
    "didOwnerReply": [9],
    "replyTextFromOwner": [9, 1]  # only if didOwnerReply is true
}