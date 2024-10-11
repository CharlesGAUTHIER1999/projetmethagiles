import tkinter as tk

# Créer la fenêtre principale
root = tk.Tk()
root.title("Exemple de Boutons Radio")

# Variable pour stocker la valeur du bouton sélectionné
choix = tk.StringVar()
choix.set("Option 1")  # Valeur par défaut

# Fonction à appeler lorsque l'utilisateur sélectionne une option
def selection():
    print("Vous avez sélectionné:", choix.get())

# Créer des boutons radio
radio1 = tk.Radiobutton(root, text="Option 1", variable=choix, value="Option 1 - G1", command=selection)
radio2 = tk.Radiobutton(root, text="Option 2", variable=choix, value="Option 2 - G1", command=selection)
radio3 = tk.Radiobutton(root, text="Option 3", variable=choix, value="Option 3 - G1", command=selection)
radio4 = tk.Radiobutton(root, text="Option 4", variable=choix, value="Option 1 - G2", command=selection)
radio5 = tk.Radiobutton(root, text="Option 5", variable=choix, value="Option 2 - G2", command=selection)
radio6 = tk.Radiobutton(root, text="Option 6", variable=choix, value="Option 3 - G2", command=selection)
radioal = tk.Radiobutton(root, text="Option 4", variable=choix, value="Tempo aléatoire", command=selection)

# Afficher les boutons radio
radio1.pack(anchor=tk.W)
radio2.pack(anchor=tk.W)
radio3.pack(anchor=tk.W)
radio4.pack(anchor=tk.W)
radio5.pack(anchor=tk.W)
radio6.pack(anchor=tk.W)
radioal.pack(anchor=tk.W)

# Lancer la boucle principale de l'application
root.mainloop()
