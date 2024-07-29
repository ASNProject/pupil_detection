import json
import os.path

import cv2
import numpy as np
import asyncio


async def main():
    def nothing(x):
        pass

    output_file = 'hsv_data.json'

    def read_json(file):
        if os.path.exists(file):
            with open(file, 'r') as json_file:
                return json.load(json_file)
        else:
            return {}

    # Baca data JSON dari file
    data = read_json(output_file)

    # Jika tidak ada data matang, inisialisasi dengan data kosong
    if 'pupil' not in data:
        data['pupil'] = {"LH": 0, "LS": 0, "LV": 0, "UH": 0, "US": 0, "UV": 0}

    # Load gambar
    image = cv2.imread('assets/images/1.png')

    # Konversi ke HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Buat jendela untuk trackbar
    cv2.namedWindow('Trackbars')

    # Buat trackbar untuk mengatur nilai HSV
    cv2.createTrackbar('LH', 'Trackbars', 0, 179, nothing)  # Lower Hue
    cv2.createTrackbar('LS', 'Trackbars', 0, 255, nothing)  # Lower Saturation
    cv2.createTrackbar('LV', 'Trackbars', 0, 255, nothing)  # Lower Value
    cv2.createTrackbar('UH', 'Trackbars', 179, 179, nothing)  # Upper Hue
    cv2.createTrackbar('US', 'Trackbars', 255, 255, nothing)  # Upper Saturation
    cv2.createTrackbar('UV', 'Trackbars', 255, 255, nothing)  # Upper Value

    while True:
        # Baca nilai trackbar
        lh = cv2.getTrackbarPos('LH', 'Trackbars')
        ls = cv2.getTrackbarPos('LS', 'Trackbars')
        lv = cv2.getTrackbarPos('LV', 'Trackbars')
        uh = cv2.getTrackbarPos('UH', 'Trackbars')
        us = cv2.getTrackbarPos('US', 'Trackbars')
        uv = cv2.getTrackbarPos('UV', 'Trackbars')
        # Definisikan rentang warna berdasarkan nilai trackbar
        lower_color = np.array([lh, ls, lv])
        upper_color = np.array([uh, us, uv])

        # Buat masker berdasarkan rentang warna
        mask = cv2.inRange(hsv_image, lower_color, upper_color)

        # Terapkan masker ke gambar asli
        result = cv2.bitwise_and(image, image, mask=mask)

        # Perbarui data json
        data['pupil']["LH"] = lh
        data['pupil']["LS"] = ls
        data['pupil']["LV"] = lv
        data['pupil']["UH"] = uh
        data['pupil']["US"] = us
        data['pupil']["UV"] = uv

        # Tampilkan hasil
        cv2.imshow('Result', result)

        print(json.dumps(data, indent=4))

        # Tunggu sampai tombol 'ESC' ditekan, kemudian tutup jendela
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            break

    # Simpan data JSON ke file
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data HSV diperbarui dan disimpan ke file: {output_file}")

    # Menutup program
    cv2.destroyAllWindows()



if __name__ == '__main__':
    asyncio.run(main())
