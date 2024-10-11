from librairie.graphique.graphique_interface import GraphiqueInterface
from ecran.ecran import Ecran
from element.clavier import Clavier
from ecran.getsionnaire_etat_ecran import GestionnaireEtatEcran
import threading
from tkinter import filedialog
import tkinter as tk

from MusicPlayer_Base import MusicPlayer as mp


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
        self.is_playing = False  # Indique si une séquence est en cours
        self.stop_requested = False  # Indique si l'arrêt a été demandé
        self.current_sound = None

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

    def play_sequence(self, filename, tempo):
        if self.is_playing:
            return  # Si la musique est déjà en cours, on ne relance pas une nouvelle lecture

        # Lancer la lecture dans un thread séparé pour éviter le blocage de l'interface
        self.is_playing = True
        self.stop_requested = False  # Réinitialise la demande d'arrêt
        threading.Thread(target=self._play_sequence_thread, args=(filename,tempo)).start()

    def _play_sequence_thread(self, filename, tempo):
        try:
            notes_sequence = []
            duration_sequence = []

            with open(filename, "r") as f:
                for line in f:
                    note = line.split()[0]
                    duration = float(line.split()[1])
                    notes_sequence.append(note)
                    duration_sequence.append(duration)

            for note, duration in zip(notes_sequence, duration_sequence):
                if self.stop_requested:
                    break  # Si l'arrêt est demandé, on quitte la boucle

                if note == "Unknown":
                    continue

                if note == "0":  # Silence
                    pygame.time.delay(int(duration * 1000 * tempo))
                    continue

                frequency = note_to_frequency.get(note, None)
                if frequency:
                    self.play(frequency, duration * tempo)

        finally:
            self.is_playing = False  # Réinitialise l'état de lecture une fois terminé

    def play(self, frequency, duration):
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
                # Synthèse additive avec plusieurs harmoniques pour imiter le son d'un piano
        tone = (0.7 * np.sin(frequency * 2 * np.pi * t) +               # Fondamentale
            0.2 * np.sin(2 * frequency * 2 * np.pi * t) +           # 1ère harmonique
            0.1 * np.sin(3 * frequency * 2 * np.pi * t) +           # 2ème harmonique
            0.05 * np.sin(4 * frequency * 2 * np.pi * t) +          # 3ème harmonique
            0.03 * np.sin(5 * frequency * 2 * np.pi * t))           # 4ème harmonique

        stereo_tone = np.vstack((tone, tone)).T
        contiguous_tone = np.ascontiguousarray((32767 * stereo_tone).astype(np.int16))
        sound = pygame.sndarray.make_sound(contiguous_tone)

        # Vérifie s'il y a déjà un son qui est joué, comme ça on le stop
        if self.current_sound:
            self.current_sound.stop()
        self.current_sound = sound
        sound.set_volume(0.05)
        sound.play()
        pygame.time.delay(int(duration * 500))

    def stop_music(self):
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None
        self.stop_requested = True  # Demande d'arrêt de la séquence
        self.is_playing = False  # Réinitialiser l'état de lecture
        
    def ajouter_bouton_radio(self):
        self.radio_var = tk.StringVar(value="Option1")  # Variable pour garder la sélection du bouton radio
        
        # Ajout du bouton radio dans frame_high
        self.radio_bouton1 = tk.Radiobutton(self.root_frame, text="Option 1", variable=self.radio_var, value="Option1")
        self.radio_bouton2 = tk.Radiobutton(self.root_frame, text="Option 2", variable=self.radio_var, value="Option2")
        
        self.radio_bouton1.pack(in_=self.bouton3, padx=5, pady=5, side="left")
        self.radio_bouton2.pack(in_=self.bouton4, padx=5, pady=5, side="left")

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
        
        frame_high = self.graphique.creer_frame(self.root_frame, bg='#cecece')
        self.message_label = tk.Label(self.root_frame, text="", fg="red")
        self.message_label.pack(padx=10, pady=10)

        self.bouton = self.graphique.creer_button(frame=frame_high, fonction=self.import_file,
                                                  label="Importation d'un fichier")
        self.bouton.pack(padx=5, pady=5, side="left")
        
        self.bouton2 = self.graphique.creer_button(frame=frame_high, fonction=self.read_random_sequence,
                                                  label="Lecture Séquence Aléatoire")
        self.bouton2.pack(padx=5, pady=5, side="left")

        self.bouton3 = self.graphique.creer_button(frame=frame_high, fonction=lambda: self.play_sequence("pirate.txt", 1), label="RUN MUSIC")
        self.bouton3.pack(padx=5, pady=5, side="left")
        self.bouton4 = self.graphique.creer_button(frame=frame_high, fonction=lambda: self.stop_music(), label="STOP MUSIC")
        self.bouton4.pack(padx=5, pady=5, side="left")    
        frame_high.pack(fill="both", expand=True)

        frame_aside = self.graphique.creer_frame(self.root_frame, bg="#FF0000")
        self.bouton1 = self.graphique.creer_button(frame=frame_aside, fonction= self.on_key_press, label="I1")
        self.bouton1.pack(padx=5, pady=5, side="left")
        self.bouton2 = self.graphique.creer_button(frame=frame_aside, fonction= self.on_key_press, label="I2")
        self.bouton2.pack(padx=5, pady=5, side="left") 
        self.bouton3 = self.graphique.creer_button(frame=frame_aside, fonction= self.on_key_press, label="I3")
        self.bouton3.pack(padx=5, pady=5, side="left")
        self.bouton4 = self.graphique.creer_button(frame=frame_aside, fonction= self.on_key_press, label="I4")
        self.bouton4.pack(padx=5, pady=5, side="left")
        self.bouton5 = self.graphique.creer_button(frame=frame_aside, fonction= self.on_key_press, label="I5")
        self.bouton5.pack(padx=5, pady=5, side="left")
        self.bouton6 = self.graphique.creer_button(frame=frame_aside, fonction= self.on_key_press, label="I6")
        self.bouton6.pack(padx=5, pady=5, side="left")
        self.bouton7 = self.graphique.creer_button(frame=frame_aside, fonction= self.on_key_press, label="I7")
        self.bouton7.pack(padx=5, pady=5, side="left")
        self.bouton8 = self.graphique.creer_button(frame=frame_aside, fonction= self.on_key_press, label="I8")
        self.bouton8.pack(padx=5, pady=5, side="left")
        frame_aside.pack(fill="both", expand=True)

        # On crée l'instance du piano
        self.clavier = Clavier(graphique=self.graphique, fenetre=frame_middle, canvas=self.canvas, largeur=50,
                               hauteur=150, top_margin=40, type='', left_margin=350, taille_bouton=14)

        # Pour afficher le piano
        frame_middle.pack(side='top', fill="x", expand=True)

        # Liaison des événements clavier
        self.ajouter_bouton_radio()

        self.fenetre_principale.bind("<Key>", self.on_key_press)

    def import_file(self):

        file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
        if file_path:

            if not file_path.lower().endswith(".txt"):
                self.message_label.config(text="Veuillez sélectionner un fichier au format .txt")
                return
            self.load_music_file(file_path)

    def read_random_sequence(self):
        # Générer une séquence aléatoire de 10 notes
        mp.generate_random_sequence(self,25, "test.txt", 1)
        self.play_sequence("test.txt", 1)
        

    def load_music_file(self, file_path):

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            self.message_label.config(text=f"Fichier {file_path} importé avec succès")

            # Jouer la séquence de musique après l'importation
            self.play_sequence(file_path, 1)

        except Exception as e:
            self.message_label.config(text=f"Erreur lors de l'importation du fichier : {e}")

    def on_key_press(self, event):
        """Callback pour jouer une note quand une touche du clavier est pressée."""
        note = self.notes_clavier.get(event.char, None)
        if note:
            frequency = note_to_frequency.get(note, None)
            if frequency:

                self.play(frequency, 0.125)  # Joue la note pendant 1 seconde
            
    def afficher(self):
        """
        Affiche la fenêtre principale.

        ----------------------------------------------------------

        """
        self.graphique.ouvrir_fenetre(self.fenetre_principale)
        