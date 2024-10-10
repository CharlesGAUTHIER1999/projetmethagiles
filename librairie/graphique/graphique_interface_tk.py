import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from librairie.graphique.graphique_interface import GraphiqueInterface


class GraphiqueInterfaceTk(GraphiqueInterface):
    def __init__(self) -> None:
        super().__init__()

    def creer_fenetre(self, titre: str, longueur: int, largeur: int, chemin_logo: str):
        """
        Création d'une fenêtre.

        ----------------------------------------------------------

        Args:
            titre (string) : le titre de la fenêtre
            longueur (int) : la longueur de la fenêtre
            largeur (int) : la largeur de la fenêtre
            chemin_logo (str) : le chemin du logo

        Return:
            fenêtre : Retourne une fenêtre tkinter.
        """
        fenetre = tk.Tk()
        fenetre.title(titre)
        longueur = str(longueur)
        largeur = str(largeur)
        fenetre.geometry(longueur + "x" + largeur)
        fenetre.iconbitmap(chemin_logo)

        return fenetre

    def creer_frame(self, fenetre: tk.Tk, bg: str = None, width: int = None, height: int = None):
        """
        Création d'un frame.

        ----------------------------------------------------------

        Args:
            fenetre (tk.Tk): la fenêtre où va apparaitre le frame (ou même un frame)
            bg (string) : la couleur du background
            width (int) : la largeur du frame
            height (int) : la hauteur du frame

        Return:
            frame : Retourne le frame créé.
        """
        frame = tk.Frame(fenetre, bg=bg, width=width, height=height)

        return frame

    def fermer_fenetre(self, fenetre: tk.Tk):
        """
        ferme une fenêtre.

        ----------------------------------------------------------

        Args:
            fenetre (tk.Tk): la fenêtre qu'on doit fermer.
        """
        fenetre.destroy()

    def ouvrir_fenetre(self, fenetre: tk.Tk):
        """
        ouvre une fenêtre.

        ----------------------------------------------------------

        Args:
            fenetre (tk.Tk): la fenêtre où va apparaitre.
        """

        fenetre.mainloop()

    def creer_button(self, frame, fonction: str, bg: str = None, activebackground: str = None, label=None,
                     image: int = None, font: int = None, width=None, height: str = None):
        """
        Création d'un bouton.

        ----------------------------------------------------------

        Args:
            frame : le frame où sera le bouton
            fonction : la fonction qu'on va utiliser pour ce bouton
            bg (string) : la couleur de l'arrière-plan du bouton
            activebackground (string) : la couleur de l'arrière-plan lors du clique
            label (str) : le label du bouton.
            image (str) : l'image, si on veut que le bouton soit en image au lieu du label
            font : le font du label
            label (str) : le label du bouton
            width (int) : la largeur du bouton
            height (int) : la hauteur du bouton

        Return:
            button : Retourne le bouton créé.
        """

        button = tk.Button(frame, width=width, height=height, text=label, cursor="hand2", image=image, command=fonction,
                           bg=bg, activebackground=activebackground, font=font)
        return button

    def creer_progress_bar(self, frame, orient: str = None, length: str = None, mode: str = None):
        """
        Création d'un progress bar.

        ----------------------------------------------------------

        Args:
            frame : le frame où sera la progress barre
            orient (str) : l'orientation de la barre
            length (string) : la longueur de la barre
            mode (str) : le mode de la barre

        Return:
            progress barre : Retourne la barre de progress créé.
        """
        progress_bar = ttk.Progressbar(frame, orient=orient, length=length, mode=mode)

        return progress_bar

    def creer_widget(self, frame, image=None, text: str = None, bg: str = None, font: str = None,
                     width: int = None, height: int = None, fg: str = None, relief: str = None,
                     padx: int = None, pady: int = None):
        """
        Création d'un widget.

        ----------------------------------------------------------

        Args:
            frame : le frame où sera le widget
            image : l'image si on veut un widget avec image
            text (string) : le text si on veut que notre widget soit en text
            bg (str) : le background du widget
            font : le font (police) du widget
            width (int) : la longueur du widget
            height (int) : la hauteur du widget
            fg :
            relief (str): le format du widget
            padx (int) : le padding x
            pady (int) : la padding y

        Return:
            progress barre : Retourne le widget créé.
        """
        # On vérifie si l'image n'est pas nul ça veut dire qu'on va mettre une image dans le widget,
        # sinon ça sera du text.
        if image is not None:
            label = tk.Label(frame, image=image, bg=bg, font=font, width=width, height=height, fg=fg, relief=relief,
                             padx=padx, pady=pady)
            return label

        elif text is not None:
            label = tk.Label(frame, text=text, bg=bg, font=font, width=width, height=height, fg=fg, relief=relief,
                             padx=padx, pady=pady)
            return label

    def creer_image(self, chemin_image: str, width: int = None, height: int = None):
        """
        Création d'une image.

        ----------------------------------------------------------

        Args:
            chemin_image (string): le chemin pour l'image
            width (int) : la largeur de l'image
            height (string) : la hauteur de l'image

        Return:
            image : Retourne l'image créée.
        """
        original_image = Image.open(chemin_image)
        resized_image = original_image.resize((width, height))
        image = ImageTk.PhotoImage(resized_image)

        return image

    def creer_canvas(self, fenetre, bg: str = None, width: int = None, height: int = None):
        """
        Création d'un canvas.

        ----------------------------------------------------------

        Args:
            fenetre : la fenêtre (ou frame) où sera placé le canvas
            bg (string) : la couleur de l'arrière-plan du canvas
            width (int) : la largeur du canvas
            height (string) : la hauteur de l'image

        Return:
            canvas : Retourne l'image créée.
        """
        canvas = tk.Canvas(fenetre, bg=bg, width=width, height=height)

        return canvas

    def creer_sous_fentre(self, fenetre):
        """
        Création d'une sous-fenêtre.

        ----------------------------------------------------------

        Args:
            fenetre : la fenêtre où sera placée la sous-fenêtre

        Return:
            fenetre (Toplevel) : Retourne la sous-fenêtre créée
        """
        return tk.Toplevel(fenetre)
