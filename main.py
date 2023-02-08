#!/usr/bin/env python
# coding: utf-8
# QR CODE GENERATOR

import qrcode
import requests
import io
import sys

from PIL import Image


def generate_qr_code(data, fill_color, bgcolor, size=(600, 600)):
  qr = qrcode.QRCode(version=1,
                     box_size=20,
                     border=2,
                     error_correction=qrcode.constants.ERROR_CORRECT_H)

  qr.add_data(data)
  qr.make(fit=True)

  img = qr.make_image(fill_color=fill_color,
                      back_color=bgcolor).convert('RGBA').resize(size)

  return img


def load_image_from_url(url):
  response = requests.get(url)

  if response.status_code == 200:
    return io.BytesIO(response.content)

  return None


def put_logo_in_qr(qr_image, logo_path, qr_back='#ffffff'):
  if logo_path.startswith('http://') or logo_path.startswith('https://'):
    image = load_image_from_url(logo_path)
    logo = Image.open(image)

    if logo is None:
      print('Invalid URL')
      return False

  else:
    logo = Image.open(logo_path)

  logo = logo.convert("RGBA")
  background = Image.new("RGBA", logo.size, (255, 255, 255, 255))
  logo = Image.alpha_composite(background, logo)
  logo = logo.convert("RGB")

  rect = (300 / float(logo.size[0]))

  logo = logo.resize((300, int((float(logo.size[1]) * float(rect)))),
                     Image.ANTIALIAS)

  position = ((qr_image.size[0] - logo.size[0]) // 2,
              (qr_image.size[1] - logo.size[1]) // 2)

  qr_image.paste(logo, position)

  return qr_image


image = generate_qr_code(data='https://bubbler.live',
                         fill_color='#08050c',
                         bgcolor='#fff',
                         size=(1000, 1000))

# If you don't need logo in the middle just comment this two line

logo_path = 'https://bubbler.live/wp-content/uploads/2021/06/cropped-bubbler-2-1.png'
image = put_logo_in_qr(image, logo_path)

image.save('new_qr_code.png')
