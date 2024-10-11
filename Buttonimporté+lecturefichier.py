import tkinter as tk
from tkinter import filedialog

class MusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VirtualMusicaLau")
        self.create_widgets()

    def create_widgets(self):
      
        import_button = tk.Button(self.root, text="Importer", command=self.import_file)
        import_button.pack(padx=10, pady=10)

        self.message_label = tk.Label(self.root, text="", fg="red")
        self.message_label.pack(padx=10, pady=10)

    def import_file(self):
       
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
        if file_path:
            
            if not file_path.lower().endswith(".txt"):
                self.message_label.config(text="Veuillez sélectionner un fichier au format .txt")
                return
            self.load_music_file(file_path)

    def load_music_file(self, file_path):
       
        self.message_label.config(text="")
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

        
            if not lines:
                self.message_label.config(text="Le fichier est vide. Veuillez fournir un fichier valide.")
                return

            
            for line_number, line in enumerate(lines, start=1):
                parts = line.strip().split()
                if len(parts) != 2:
                    self.message_label.config(text=f"Erreur de format à la ligne {line_number} : {line.strip()}")
                    return
                note, duration = parts

              
                try:
                    duration = float(duration)
                except ValueError:
                    self.message_label.config(text=f"Durée invalide à la ligne {line_number} : {duration}")
                    return

                if note != "0" and note != "Unknown" and not note.isalnum():
                    self.message_label.config(text=f"Note invalide à la ligne {line_number} : {note}")
                    return

         
            self.message_label.config(text=f"Fichier {file_path} importé avec succès")
          

        except Exception as e:
            self.message_label.config(text=f"Erreur lors de l'importation du fichier : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x200")
    app = MusicApp(root)
    root.mainloop()
