# Pupil Detection

Python version
```
'3.10.6'
```

### Run Project
Clone project
```
https://github.com/ASNProject/pupil_detection.git
```

Install requirements.txt
```
pip install -r requirements.txt
```

Run Project 
```
python main.py
```

Result: https://youtu.be/E5N95Bou5mQ

Note:
- Jika menggunakan Raspberry silahkan buat env terlebih dahulu (Ini hanya dilakukan 1 kali jika belum memiliki env)
```
python -m venv env
```
- Kemudian jalankan env yang sudah dibuat (Jalankan env ketika sebelum menjalankan program)
```
source env/bin/activate
```

### Optional
Jika dirasa akurasi kurang maksimal silahkan kalibrasi menggunakan HSV calibration dengan  menjalankan script
```
python calibration.py
```

setelah selesai setting HSV silahkan tekan "ESC" pada keyboard untuk keluar

Link tutorial: [Kalibrasi](https://youtu.be/I8AkaV3S8_k)