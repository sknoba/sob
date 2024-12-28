import random
import string
import uuid

INDIAN_STATES = [
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CT', 'Chhattisgarh'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OR', 'Odisha'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TG', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UT', 'Uttarakhand'),
    ('WB', 'West Bengal'),
    ('AN', 'Andaman and Nicobar Islands'),
    ('CH', 'Chandigarh'),
    ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('LD', 'Lakshadweep'),
    ('DL', 'Delhi'),
    ('JK', 'Jammu and Kashmir'),
    ('LA', 'Ladakh'),
    ('PY', 'Puducherry')
]

def generate_random_number(length=4, alpha=False):
    if alpha:
        # Generate a random alphanumeric string of the specified length
        characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
        return ''.join(random.choice(characters) for _ in range(length)).upper()
    else:
        # Generate a random numeric value of the specified length
        min_value = 10**(length - 1)  # The smallest number with the specified number of digits
        max_value = 10**length - 1    # The largest number with the specified number of digits
        return random.randint(min_value, max_value)
    

import random
from  django.apps import apps

def generate_sub_code():
    while True:        
        code = str(random.randint(1000, 9999))
        subject = apps.get_model('core', 'Subject')                
        if not subject.objects.filter(code=code).exists():
            return code
        