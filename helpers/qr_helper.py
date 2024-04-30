

import string, random

def qr_code_generator(size=6,chars=f"{string.ascii_uppercase}{string.digits}"):
    return ''.join(random.choice(chars) for _ in range(size))



