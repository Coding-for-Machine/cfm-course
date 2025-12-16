import random
import string

def generate_slug_with_case(length=8):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    slug = 'cfm-'
    for _ in range(length):
        slug += random.choice(characters)
    return slug
