
from librairie.graphique.graphique_interface import GraphiqueInterface


class PlateauJeu:
    def __init__(self, graphique: GraphiqueInterface, fenetre, canvas, type: str, largeur: int,
                 hauteur: int, top_margin: int, left_margin: int, taille_bouton: int):
        self.graphique = graphique
        self.fenetre_plateau = fenetre
        self.canvas = canvas
        self.type = type

        self.create_piste(largeur, hauteur, top_margin, left_margin, taille_bouton)

    def create_piste(self, largeur: int, hauteur: int, top_margin: int, left_margin: int, taille_bouton: int) -> None:
        # Largeur d'une case
        largeur_case = largeur

        # Hauteur d'une case
        hauteur_case = hauteur

        # On ajoute un peu de margin pour que la piste ne soit pas coller en haut
        # Du coup sur y2 on doit faire top_margin + la valeur de la fin du rectangle.
        top_margin = top_margin

        # Marge à gauche du canvas
        # On va faire l'addition dans x1 et x2 pour décaler à droite
        left_margin = left_margin

        # Création des cases de la piste
        for i in range(taille_bouton):

            x1 = left_margin + i * largeur_case
            y1 = top_margin
            x2 = left_margin + (i + 1) * largeur_case
            y2 = top_margin + hauteur_case
            if self.type == "btn_down":
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black", tags="case")
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text='', font=("Helvetica", 10))

            if self.type == "btn_up":
                x1 = (left_margin + 20) + i * (largeur_case -2)
                y1 = top_margin
                x2 = left_margin + (i + 1) * (largeur_case - 2)
                y2 = top_margin + (hauteur_case - 20)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black", tags="case")
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text='', font=("Helvetica", 10))
