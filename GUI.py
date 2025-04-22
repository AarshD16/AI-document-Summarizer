import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import ttk, messagebox
from backend import summarize_pdf
from PIL import Image, ImageTk, ImageSequence
import threading


class PDFSummarizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tk.call('tk', 'scaling', 1.2)  # For DPI-aware scaling

        self.title("PDF Summarizer using LLAMA3")
        self.geometry("850x550")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width=850, height=550, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frames = []
        self.load_gif("background.gif")
        self.animate(0)

        self.create_widgets()

    def load_gif(self, gif_path):
        gif = Image.open(gif_path)
        for frame in ImageSequence.Iterator(gif):
            frame = frame.resize((850, 550), Image.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(frame))

    def animate(self, counter):
        frame = self.frames[counter]
        self.bg_label.configure(image=frame)
        self.after(80, lambda: self.animate((counter + 1) % len(self.frames)))

    def create_widgets(self):
        # Semi-transparent purple overlay panel
        overlay = tk.Frame(self, bg='#200033', bd=0, highlightthickness=0)
        overlay.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

        tk.Label(
            overlay,
            text="PDF Summarizer",
            font=("Segoe UI", 16, "bold"),
            fg="#cccccc",
            bg="#200033"
        ).pack(pady=(30, 5))

        tk.Label(
            overlay,
            text="PDF Summarizer using LLAMA3 🦙",
            font=("Segoe UI", 22, "bold"),
            fg="#ffffff",
            bg="#200033"
        ).pack(pady=10)

        choose_btn = tk.Button(
            overlay,
            text="Choose PDF File",
            command=self.choose_file,
            font=("Segoe UI", 14, "bold"),
            bg="#cf32ff",
            fg="white",
            activebackground="#aa29e5",
            activeforeground="white",
            bd=0,
            relief="flat",
            padx=20,
            pady=10
        )
        choose_btn.configure(cursor="hand2")
        choose_btn.pack(pady=10)

        self.status_label = tk.Label(
            overlay,
            text="",
            font=("Segoe UI", 12),
            fg="#dddddd",
            bg="#200033"
        )
        self.status_label.pack(pady=(20, 5))

        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#2d003d",
            bordercolor="#2d003d",
            background="#ff66c4",
            lightcolor="#cc5eff",
            darkcolor="#933fff"
        )

        self.progress_bar = ttk.Progressbar(
            overlay,
            style="Custom.Horizontal.TProgressbar",
            orient="horizontal",
            length=500,
            mode="indeterminate"
        )
        self.progress_bar.pack(pady=10)

        self.summary_label = tk.Label(
            overlay,
            text="",
            font=("Segoe UI", 12, "italic"),
            fg="#89e0ff",
            bg="#200033"
        )
        self.summary_label.pack(pady=(5, 10))

        self.output_box = scrolledtext.ScrolledText(
            overlay,
            width=90,
            height=10,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg="#200033",
            fg="#b3f8ff",
            insertbackground="white",
            relief="flat",
            borderwidth=2,
            highlightbackground="#4d0073",
            highlightthickness=1
        )
        self.output_box.pack(padx=10, pady=15)
        self.output_box.config(state='disabled')

    def choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.status_label.config(text="Processing PDF and generating...")
            self.summary_label.config(text="")
            self.output_box.config(state='normal')
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, "⏳ Generating summary using LLaMA3...\n")
            self.output_box.config(state='disabled')
            self.progress_bar.start()
            threading.Thread(target=self.generate_summary, args=(file_path,)).start()

    def generate_summary(self, file_path):
        try:
            summary = summarize_pdf(file_path)
            self.output_box.config(state='normal')
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, summary)
            self.output_box.config(state='disabled')
            self.status_label.config(text="✅ Summary ready!")
            self.summary_label.config(text="Summary generated using LLaMA3.")
        except Exception as e:
            self.status_label.config(text="❌ Error while generating summary.")
            messagebox.showerror("Error", str(e))
        finally:
            self.progress_bar.stop()


if __name__ == "__main__":
    app = PDFSummarizerApp()
    app.mainloop()
