from librairie.graphique.graphique_interface import GraphiqueInterface
from ecran.ecran import Ecran
from element.plateau import Clavier
from MusicPlayer_Base import MusicPlayer
from ecran.getsionnaire_etat_ecran import GestionnaireEtatEcran

from note_frequence_base import note_to_frequency


import numpy as np
import pygame


class EcranPrincipal(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran, sample_rate=44100):
        """
        Initialise la classe EcranPrincipal.
        ----------------------------------------------------------

        Args:
            self (EcranGameBasic) : l'instance de la classe ViewPlateau.
            graphique (GraphiqueInterface) : l'instance de la classe GraphiqueInterface.
            gestionnaire_etat_ecran (GestionnaireEtatEcran) : l'instance de la classe GestionnaireEtatEcran.

        """
        # On l'initialise à None pour pouvoir rentrer dans la fonction initialiser
        super().__init__()
        self.fenetre_principale = None
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.graphique = graphique

        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        self.sample_rate = sample_rate

        self.notes_clavier = {
            # blanches
            'a': 'C4',
            'z': 'D4',
            'e': 'E4',
            'r': 'F4',
            't': 'G4',
            'y': 'A4',
            'u': 'B4',
            'w': 'C5',
            'x': 'D5',
            'c': 'E5',
            'v': 'F5',
            'b': 'G5',
            'n': 'A5',
            ',': 'B5',
            # Noires
            'é': 'C#4',
            '"': 'D#4',
            '(': 'F#4',
            '-': 'G#4',
            'è': 'A#4',
            's': 'C#5',
            'd': 'D#5',
            'g': 'F#5',
            'h': 'G#5',
            'j': 'A#5',
        }

    # c'est le tone passé en entrée qu'il faudra modifier en fonction de l'instrument joué
    # cette méthode pourra être appelée ensuite quelque soit l'instrument choisi
    def _play_tone(self, tone, duration):
        stereo_tone = np.vstack((tone, tone)).T
        contiguous_tone = np.ascontiguousarray((32767 * stereo_tone).astype(np.int16))
        sound = pygame.sndarray.make_sound(contiguous_tone)
        sound.set_volume(0.05)  # Réglez le volume
        sound.play()
        pygame.time.delay(int(duration * 1000)) # tenir la note la durée voulue

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
        Initialise l'interface de la fenêtre EcranPrincipal.

        ----------------------------------------------------------
        """
        self.fenetre_principale = self.graphique.creer_fenetre("Fenêtre Principale", 1400, 800, "")

        self.root_frame = self.graphique.creer_frame(self.fenetre_principale, bg="#fff")
        self.root_frame.pack(fill='both', expand=True)

        # Le frame pour les éléments du milieu (le piano)
        frame_middle = self.graphique.creer_frame(self.root_frame, bg="#fff")

        self.canvas = self.graphique.creer_canvas(frame_middle, bg="#fff")
        self.canvas.pack(fill="both", expand=True)

        # On crée l'instance du piano
        self.clavier = Clavier(graphique=self.graphique, fenetre=frame_middle, canvas=self.canvas, largeur=30,
                               hauteur=150, top_margin=40, type='', left_margin=350, taille_bouton=14)

        # Pour afficher le piano
        frame_middle.pack(side='top', fill="x", expand=True)

        # On attend pour lancer la musique
        # self.fenetre_principale.after(200, self.lancer_musique)

        # Liaison des événements clavier
        self.fenetre_principale.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        """Callback pour jouer une note quand une touche du clavier est pressée."""
        note = self.notes_clavier.get(event.char, None)
        if note:
            frequency = note_to_frequency.get(note, None)
            if frequency:
                self.play(frequency, 1)  # Joue la note pendant 1 seconde

    def lancer_musique(self):
        ml = MusicPlayer()
        ml.play(note_to_frequency["F7"], 1)
        ml.play(note_to_frequency["B3"], 4)
        ml.play(note_to_frequency["E5"], 0.5)
            
    def afficher(self):
        """
        Affiche la fenêtre principale.

        ----------------------------------------------------------

        """
        self.graphique.ouvrir_fenetre(self.fenetre_principale)
