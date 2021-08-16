# source: https://registry-page.isdcf.com/contenttypes/

# A theatrical feature.
FEATURE = "FTR"

# Short (2 to 3 minutes) content promoting an upcoming theatrical feature.
TRAILER = "TLR"

# Very short (typically less than 1 minute) content promoting an upcoming theatrical feature.
TEASER = "TSR"

# Content used to test, calibrate or setup D-Cinema exhibition equipment.
TEST = "TST"

# Slate/still picture indicating the recommended age group permitted to view the content to follow.
# This rating is generally unique per country.
RATING = "RTG"

# Content promoting a product or service other than an upcoming feature.
ADVERTISEMENT = "ADV"

# Non advertising/promotional content (3 to 15 minutes) typically before a theatrical feature.
SHORT = "SHR"

# Extremely short content (1 to 15 seconds) separating unrelated compositions.
TRANSITIONAL = "XSN"

# Public service announcement.
PSA = "PSA"

together = {
    "Feature": FEATURE,
    "Trailer": TRAILER,
    "Teaser": TEASER,
    "Test": TEST,
    "Rating": RATING,
    "Advertisement": ADVERTISEMENT,
    "Short": SHORT,
    "Transitional": TRANSITIONAL,
    "PSA": PSA
}
