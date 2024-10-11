
from librairie.graphique.graphique_interface import GraphiqueInterface


class Clavier:
    def __init__(self, graphique: GraphiqueInterface, fenetre, canvas, type: str, largeur: int,
                 hauteur: int, top_margin: int, left_margin: int):
        self.graphique = graphique
        self.fenetre_plateau = fenetre
        self.canvas = canvas
        self.type = type

        # Dictionnaire pour stocker les touches
        self.touches = {}
        self.list_touches_blanche = ['a', 'z', 'e', 'r', 't', 'y', 'u', 'v', 'b', 'n', ',', ';', ':', '!']
        self.list_touches_noire = ['é', '"', '(', '-', 'è', 'g', 'h', 'k', 'l', 'm']

        self.create_clavier_piano(largeur, hauteur, top_margin, left_margin)

    def create_clavier_piano(self, largeur: int, hauteur: int, top_margin: int, left_margin: int) -> None:
        # Dimensions des touches
        largeur_touche_blanche = largeur
        hauteur_touche_blanche = hauteur
        largeur_touche_noire = largeur // 1.5
        hauteur_touche_noire = hauteur // 1.5

        # Index pour les touches noires
        noire_index = 0

        # Création des touches blanches
        for i, key in enumerate(self.list_touches_blanche):
            x1 = left_margin + i * largeur_touche_blanche
            y1 = top_margin
            x2 = x1 + largeur_touche_blanche
            y2 = y1 + hauteur_touche_blanche

            touche_blanche = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
            self.touches[key] = touche_blanche  # Associe la touche blanche à son ID

            # Création des touches noires (aux bons endroits seulement)
            if i % 7 in [0, 1, 3, 4, 5]:  # Ces indices correspondent aux positions où il y a une touche noire
                x1_noir = x1 + largeur_touche_blanche * 0.75  # Position décalée vers la droite
                y1_noir = top_margin
                x2_noir = x1_noir + largeur_touche_noire
                y2_noir = y1_noir + hauteur_touche_noire

                touche_noire = self.canvas.create_rectangle(x1_noir, y1_noir, x2_noir, y2_noir, fill="black",
                                                            outline="black", tags="touche_noire")

                # Associer la touche noire à une lettre
                if noire_index < len(self.list_touches_noire):
                    touche_clavier_noire = self.list_touches_noire[noire_index]
                    self.touches[touche_clavier_noire] = touche_noire
                    # On incrémente la prochaine touche noire
                    noire_index += 1
