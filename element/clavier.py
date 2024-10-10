
from librairie.graphique.graphique_interface import GraphiqueInterface


class Clavier:
    def __init__(self, graphique: GraphiqueInterface, fenetre, canvas, type: str, largeur: int,
                 hauteur: int, top_margin: int, left_margin: int, taille_bouton: int):
        self.graphique = graphique
        self.fenetre_plateau = fenetre
        self.canvas = canvas
        self.type = type

        self.create_clavier_piano(largeur, hauteur, top_margin, left_margin, taille_bouton)

    def create_clavier_piano(self, largeur: int, hauteur: int, top_margin: int, left_margin: int, nb_touches: int) -> None:
        # Dimensions des touches
        largeur_touche_blanche = largeur
        hauteur_touche_blanche = hauteur
        largeur_touche_noire = largeur // 1.5
        hauteur_touche_noire = hauteur // 1.5

        # Création des touches blanches
        for i in range(nb_touches):
            x1 = left_margin + i * largeur_touche_blanche
            y1 = top_margin
            x2 = x1 + largeur_touche_blanche
            y2 = y1 + hauteur_touche_blanche

            # Dessin des touches blanches
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black", tags="touche_blanche")
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, font=("Helvetica", 10))

            # Création des touches noires (2e, 4e, 6e, 9e, et 11e sur 12 touches)
            if i % 7 in [0, 1, 3, 4, 5]:  # Ces indices correspondent aux positions où il y a une touche noire
                x1_noir = x1 + largeur_touche_blanche * 0.75  # Position décalée vers la droite
                y1_noir = top_margin
                x2_noir = x1_noir + largeur_touche_noire
                y2_noir = y1_noir + hauteur_touche_noire

                # Dessin des touches noires
                self.canvas.create_rectangle(x1_noir, y1_noir, x2_noir, y2_noir, fill="black", outline="black",
                                             tags="touche_noire")