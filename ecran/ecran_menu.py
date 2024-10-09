from librairie.graphique.graphique_interface import GraphiqueInterface
from ecran.ecran import Ecran
from element.plateau import PlateauJeu
from ecran.getsionnaire_etat_ecran import GestionnaireEtatEcran

import numpy as np
import pygame


class EcranPrincipale(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran, sample_rate=44100):
        """
        Initialise la classe EcranPrincipale.
        ----------------------------------------------------------

        Args:
            self (EcranGameBasic) : l'instance de la classe ViewPlateau.
            graphique (GraphiqueInterface) : l'instance de la classe GraphiqueInterface.
            gestionnaire_etat_ecran (GestionnaireEtatEcran) : l'instance de la classe GestionnaireEtatEcran.

        """
        # On l'initialise à None pour pouvoir rentrer dans la fonction initialiser
        super().__init__()
        self.fenetre_menu = None
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.graphique = graphique

        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        self.sample_rate = sample_rate

    # c'est le tone passé en entrée qu'il faudra modifier en fonction de l'instrument joué
    # cette méthode pourra être appelée ensuite quelque soit l'instrument choisis
    def _play_tone(self, tone, duration):
        stereo_tone = np.vstack((tone, tone)).T
        contiguous_tone = np.ascontiguousarray((32767 * stereo_tone).astype(np.int16))
        sound = pygame.sndarray.make_sound(contiguous_tone)
        sound.set_volume(0.05)  # Réglez le volume
        sound.play()
        pygame.time.delay(int(duration * 1000)) #tenir la note la durée voulue

    # Exemple de tonalité, extraire ce qui va bien pour pouvoir faire varier, pour simuler différents instruments
    def play(self, frequency, duration):
        # Créer une onde sinusoïdale à la fréquence spécifiée
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone = np.sin(frequency * 2 * np.pi * t)

        # Créer un tableau stéréo (2D) en dupliquant le ton
        stereo_tone = np.vstack((tone, tone)).T

        # S'assurer que le tableau est contigu en mémoire
        contiguous_tone = np.ascontiguousarray((32767 * stereo_tone).astype(np.int16))

        # Convertir l'onde sinusoïdale en un format audio et jouer
        sound = pygame.sndarray.make_sound(contiguous_tone)
        sound.set_volume(0.05)  # Réglez le volume
        sound.play()
        pygame.time.delay(int(duration * 500)) 


    def initialiser_interface(self):
        """
        Initialise l'interface de la fenêtre EcranPrincipale.

        ----------------------------------------------------------
        """
        self.fenetre_menu = self.graphique.creer_fenetre("Fenêtre Principale", 1400, 800, "")

        self.root_frame = self.graphique.creer_frame(self.fenetre_menu, bg="#fff")
        self.root_frame.pack(fill='both', expand=True)


        # Le frame pour les éléments du milieu (le piano)
        frame_middle = self.graphique.creer_frame(self.root_frame, bg="#fff")

        self.canvas = self.graphique.creer_canvas(frame_middle, bg="#fff")
        self.canvas.pack(fill="both", expand=True)

        # On crée l'instance du piano
        self.plateau = PlateauJeu(graphique=self.graphique, fenetre=frame_middle, canvas=self.canvas, type="btn_down",
                                  largeur=60, hauteur=80, top_margin=100, left_margin=175, taille_bouton=14)

        self.plateau = PlateauJeu(graphique=self.graphique, fenetre=frame_middle, canvas=self.canvas, type="btn_up",
                                  largeur=50, hauteur=80, top_margin=100, left_margin=175, taille_bouton=5)
        

        # Pour afficher le piano
        frame_middle.pack(side='top', fill="x", expand=True)

            
    def afficher(self):
        """
        Affiche la fenêtre principale.

        ----------------------------------------------------------

        """
        self.graphique.ouvrir_fenetre(self.fenetre_menu)
