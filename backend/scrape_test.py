import urllib.request
import json
import re

def get_image_url(query):
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query + " product image")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # Try to find any image URL in the duckduckgo result (often they use proxy, but it's an image)
        match = re.search(r'<img[^>]+src="([^"]+)"', html)
        if match:
            src = match.group(1)
            if src.startswith('//'):
                return "https:" + src
            return src
    except Exception as e:
        pass
    return f"https://placehold.co/600x400/E2E8F0/475569?text={urllib.parse.quote(query)}"

if __name__ == "__main__":
    print(get_image_url("Dot & Key Barrier Repair Moisturizer"))
