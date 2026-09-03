import hashlib
import json
from pathlib import Path
from pypdf import PdfReader

root = Path('.')
out = root / 'images' / 'catalogue'
out.mkdir(parents=True, exist_ok=True)
reader = PdfReader('Catalogue Q3 - UPDATED.pdf')
seen = {}
page_assets = {}

def extension(data):
    if data.startswith(b'\x89PNG'):
        return 'png'
    if data.startswith(b'\xff\xd8'):
        return 'jpg'
    if data.startswith(b'GIF8'):
        return 'gif'
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'webp'
    return None

for page_number, page in enumerate(reader.pages, 1):
    assets = []
    for image in page.images:
        data = image.data
        if len(data) < 10000:
            continue
        digest = hashlib.sha1(data).hexdigest()[:12]
        file_extension = extension(data)
        if not file_extension:
            continue
        if digest not in seen:
            filename = f'catalogue-{len(seen) + 1:04d}.{file_extension}'
            (out / filename).write_bytes(data)
            seen[digest] = filename
        assets.append(seen[digest])
    page_assets[page_number] = list(dict.fromkeys(assets))

products_path = root / 'js' / 'products.js'
source = products_path.read_text(encoding='utf-8')
products = json.loads(source[source.index('['):source.index('];') + 1])
page_texts = [page.extract_text() or '' for page in reader.pages]
for product in products:
    product_pages = [index + 1 for index, text in enumerate(page_texts) if product['id'] in text]
    asset = next((page_assets[page][0] for page in product_pages if page_assets.get(page)), None)
    if asset:
        product['image'] = f'images/catalogue/{asset}'

products_path.write_text(
    '// Imported from Catalogue Q3 - UPDATED.pdf. Local images extracted from the catalogue.\n'
    + 'const products = ' + json.dumps(products, ensure_ascii=True, indent=2)
    + ';\nfunction getProduct(id) { return products.find(product => product.id === id); }\n'
    + "function money(value) { return `&#8358;${value.toLocaleString('en-NG')}`; }\n",
    encoding='utf-8'
)
print(f'unique images {len(seen)}; products {len(products)}; mapped {sum(p["image"].startswith("images/") for p in products)}')
