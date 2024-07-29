import cv2
import tkinter as tk
from PIL import Image, ImageTk


class CameraApp:
    def __init__(self, window):
        self.hsv_ranges = None
        self.window = window
        self.window.title("Pupil Detection")
        self.window.geometry("1320x480")  # Menyesuaikan ukuran window untuk dua kamera

        # Membuka kamera
        self.cap1 = cv2.VideoCapture(0)

        # Lebar dan tinggi maksimum untuk gambar
        self.max_width = 620
        self.max_height = 360

        # Label untuk menampilkan video dari kamera
        self.label1 = tk.Label(window)
        self.label1.place(x=20, y=20, width=self.max_width, height=self.max_height)

        # Label untuk menampilkan gambar hasil capture
        self.captured_label = tk.Label(window)
        self.captured_label.place(x=680, y=20, width=self.max_width, height=self.max_height)

        # Tombol untuk menangkap gambar
        self.capture_button = tk.Button(window, text="Capture", command=self.capture_frame)
        self.capture_button.place(x=20, y=420)

        # Mulai proses pembacaan gambar dari kamera
        self.show_frame()

    def show_frame(self):
        # Baca frame dari kamera
        ret1, frame1 = self.cap1.read()

        if ret1:
            # Proses dan tampilkan frame dari kamera 1
            img1 = self.convert_to_tk_image(frame1)
            self.label1.imgtk = img1
            self.label1.configure(image=img1)

        # Panggil fungsi ini lagi setelah 10 milidetik
        self.label1.after(10, self.show_frame)

    def capture_frame(self):
        # Baca frame dari kamera
        ret, frame = self.cap1.read()

        if ret:
            # Convert frame to ImageTk format
            capture_image = self.convert_to_tk_image(frame)
            # Tampilkan gambar hasil capture
            self.captured_label.imgtk = capture_image
            self.captured_label.configure(image=capture_image)

    def convert_to_tk_image(self, frame):
        # Convert frame to ImageTk format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img.thumbnail((self.max_width, self.max_height), Image.LANCZOS)
        return ImageTk.PhotoImage(image=img)

    def on_closing(self):
        self.cap1.release()
        self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
