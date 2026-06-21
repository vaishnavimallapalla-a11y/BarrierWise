import re

with open('seed.py', 'r', encoding='utf-8') as f:
    content = f.read()

def repl(m):
    line = m.group(0)
    if 'key_ingredients' not in line:
        lower_line = line.lower()
        if 'serum' in lower_line:
            ing = '"Hyaluronic Acid, Vitamin C"'
        elif 'cleanser' in lower_line:
            ing = '"Salicylic Acid, Ceramides"'
        elif 'shampoo' in lower_line:
            ing = '"Keratin, Tea Tree Oil"'
        elif 'conditioner' in lower_line or 'mask' in lower_line:
            ing = '"Argan Oil, Shea Butter"'
        elif 'moisturizer' in lower_line:
            ing = '"Glycerin, Squalane"'
        elif 'sunscreen' in lower_line:
            ing = '"Zinc Oxide, Titanium"'
        elif 'toner' in lower_line:
            ing = '"Rose Water, Witch Hazel"'
        else:
            ing = '"Aloe Vera, Niacinamide"'
        
        line = line.replace('"image_url":', f'"key_ingredients": {ing}, "image_url":')
    return line

new_content = re.sub(r'\{"name":.*?\}', repl, content)

with open('seed.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("seed.py patched with key ingredients!")
