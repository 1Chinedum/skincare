# UKCosmetics

A lightweight static skincare and beauty catalog for an independent Oriflame partner/consultant.

## Run locally

Open `index.html` directly in a browser, or serve the folder with any static web server. No build step or backend is required.

## Add products

Edit the `products` array in `js/products.js`. Each product has an ID, name, price, image, category, description, benefits, usage, ingredients, availability, and featured flag. Product images extracted from the catalogue are stored directly in the project root alongside the website files.

To repeat the image import after receiving a new PDF, place it beside `extract_images.py` with the expected catalogue filename and run `python extract_images.py`.

## WhatsApp ordering

Orders are sent through WhatsApp click-to-chat to the provided Nigerian number `08034904908`, converted in code to international format.

Replace the supplied placeholders for business name, owner, email, and location before publishing.

