import os
from tkinter import Tk, Label, Button, filedialog, Listbox, END, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image

class GifCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Drag & Drop GIF Creator")
        self.root.geometry("400x500")

        Label(root, text="Drag & Drop or Add Images", font=("Arial", 12)).pack(pady=10)

        self.listbox = Listbox(root, width=50, height=10)
        self.listbox.pack(pady=10)
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.drag_drop)

        Button(root, text="Add Images", command=self.add_images).pack(pady=5)
        Button(root, text="Remove Images", command=self.remove_selected).pack(pady=5)
        Button(root, text="Create GIF", command=self.create_gif).pack(pady=10)

        self.images = []

    def drag_drop(self, event):

        drop_files = self.root.tk.splitlist(event.data)  

        for file in drop_files:
            file = file.strip('{}')
            normalized_path = os.path.normpath(file.strip('{}'))
            if normalized_path not in self.images:
                self.images.append(normalized_path)
                self.listbox.insert("end", normalized_path)

    def add_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        for file in files:
            normalized_path = os.path.normpath(file)
            if normalized_path not in self.images:
                self.images.append(normalized_path)
                self.listbox.insert(END, normalized_path)

    def remove_selected(self):
        for index in reversed(self.listbox.curselection()):
            del self.images[index]
            self.listbox.delete(index)

    def create_gif(self):
        if not self.images:
            messagebox.showerror("Error", "No images selected!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
        if not save_path:
            return

        try:
            images = [Image.open(img).convert("RGBA") for img in self.images]
            base_width, base_height = images[0].size
            resized_images = [img.resize((base_width, base_height), Image.Resampling.LANCZOS) for img in images]

            resized_images[0].save(
                save_path,
                save_all=True,
                append_images=resized_images[1:],
                duration=500,
                loop=0
            )

            messagebox.showinfo("Success", f"GIF saved at {save_path}")

        except FileNotFoundError as e:
            messagebox.showerror("Error", f"File not found: {e}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    GifCreator(root)
    root.mainloop()
