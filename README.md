# DEVELOPMENT OF THIS PROJECT HAS MOVED
https://github.com/toxygene/random-proxy-printer

# Random Proxy Printer

TODO photo of box here
TODO photo of box insides here

This program uses a seven segment display, rotary encoder, and thermal printer to allow users to select a value and print a random proxy based on that value.

## Setup



## FAQ

* The proxies table is empty. How do I populate it?

I will not provide code to populate the proxies table in the database -- it would be a violation of the intellectual property of the company that owns the data.

* The fan policy for *[insert game here]* allows printing of proxies, can you include code to generate a proxies table for it?

No. This repository will not include any IP-related code. I am willing to link to any projects that create the proxies database, as long as it clearly does not violate any IP.

* Why publicly post the code if you aren't going to include the code to use it?

During the development of this project, I had to cross reference a lot of sparce documentation to get things working. It was frequently frustrating to figure out how to tie together all the pieces the way I wanted them. This Github project is as much a work log and amalgamation of the things I learned as it is a finished product.

* How can I add my own proxies to the database?

The code needs an SQLite3 database with the structure defined in `ddl.sql`. You can create your own SQLite3 database and update the systemd configuration to use it.

There are a few requirements of the data in the `description` and `illustration` fields.

The `description` must be in ASCII.

The `illustration` must be a format supported by [Pillow](https://pillow.readthedocs.io/). If you are using the CSN-A2 thermal printer, the `illustration` must also have a width <= 384 pixels. If you are using a non-color printer, I recommend converting the image to grayscale, then quantizing the palette to 8 colors.

Alternatively, if you store the `description` in UTF-8, and the `illustration` is any format supported by Python [Pillow](https://pillow.readthedocs.io/), you can use the `bin/convert-database.py` script. It will convert every `description` from UTF-8 to ASCII, and update the `illustration` to be a max. width of 384 pixels, convert it to grayscale, quantize it to 8 colors, and save it as an optimized PNG.
