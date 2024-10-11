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
from MusicPlayer_Base import MusicPlayer as mp
import re


class EcranPrincipal(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran, sample_rate=44100):
        super().__init__()
        self.fenetre_principale = None
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.graphique = graphique
        self.is_playing = False
        # Indique si l'arrêt a été demandé
        self.stop_requested = False
        self.touches_piano = {}
        self.current_sound = None

        self.fonctionRand = None
        self.fonctionRand2 = None

        pygame.mixer.init(frequency=sample_rate, size=-16, channels=2)
        self.sample_rate = sample_rate

        # Mappage des touches du clavier aux notes de piano
        self.notes_clavier = {
            # blanches
            'a': 'C4',
            'z': 'D4',
            'e': 'E4',
            'r': 'F4',
            't': 'G4',
            'y': 'A4',
            'u': 'B4',
            'v': 'C5',
            'b': 'D5',
            'n': 'E5',
            ',': 'F5',
            ';': 'G5',
            ':': 'A5',
            '!': 'B5',
            # Noires
            'é': 'C#4',
            '"': 'D#4',
            '(': 'F#4',
            '-': 'G#4',
            'è': 'A#4',
            'g': 'C#5',
            'h': 'D#5',
            'k': 'F#5',
            'l': 'G#5',
            'm': 'A#5',
        }

    def _play_tone(self, tone, duration):
        stereo_tone = np.vstack((tone, tone)).T
        contiguous_tone = np.ascontiguousarray((32767 * stereo_tone).astype(np.int16))
        sound = pygame.sndarray.make_sound(contiguous_tone)
        sound.set_volume(0.05)  
        sound.play()
        pygame.time.delay(int(duration * 1000))

    def play_sequence(self, filename, tempo):
        print("tempo1", tempo)
        if self.is_playing:
            return  # Empêcher de relancer une lecture si une séquence est en cours
        self.is_playing = True
        self.stop_requested = False  # Réinitialise la demande d'arrêt
        threading.Thread(target=self._play_sequence_thread, args=(filename, tempo)).start()

    def _play_sequence_thread(self, filename, tempo):
        print("tempo2", tempo)

        if tempo == "60":
            print("tempo 60")
            tempo = 2
        elif tempo == "90":
            print("tempo 90")
            tempo = 1
        elif tempo == "120":
            print("tempo 120")
            tempo = 0.5
        try:
            notes_sequence, duration_sequence = [], []
            with open(filename, "r") as f:
                for line in f:
                    note, duration = line.split()
                    notes_sequence.append(note)
                    duration_sequence.append(float(duration))

            for note, duration in zip(notes_sequence, duration_sequence):
                if self.stop_requested:
                    break  # Si l'arrêt est demandé, on quitte la boucle

                if note == "Unknown":
                    continue

                if note == "0":  # Silence
                    pygame.time.delay(int(duration * 1000 * float(tempo)))

                    continue

                frequency = note_to_frequency.get(note, None)
                if frequency:
                    self.play(frequency, duration * float(tempo))
        finally:
            self.is_playing = False  

    def play(self, frequency, duration):
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone = (0.7 * np.sin(frequency * 2 * np.pi * t) +
                0.2 * np.sin(2 * frequency * 2 * np.pi * t) +
                0.1 * np.sin(3 * frequency * 2 * np.pi * t) +
                0.05 * np.sin(4 * frequency * 2 * np.pi * t) +
                0.03 * np.sin(5 * frequency * 2 * np.pi * t))

        stereo_tone = np.vstack((tone, tone)).T
        contiguous_tone = np.ascontiguousarray((32767 * stereo_tone).astype(np.int16))
        sound = pygame.sndarray.make_sound(contiguous_tone)

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
        self.stop_requested = True
        self.is_playing = False

    def initialiser_interface(self):
        self.fenetre_principale = self.graphique.creer_fenetre("Fenêtre Principale", 1400, 800, "")
        self.root_frame = self.graphique.creer_frame(self.fenetre_principale, bg="#fff")
        self.root_frame.pack(fill='both', expand=True)

        frame_middle = self.graphique.creer_frame(self.root_frame, bg="#fff")
        self.canvas = self.graphique.creer_canvas(frame_middle, bg="#fff")
        self.canvas.pack(fill="both", expand=True)
        
        frame_high = self.graphique.creer_frame(self.root_frame, bg='#cecece')
        self.frame_high_left = self.graphique.creer_frame(frame_high, bg='#cecece')
        self.frame_high_right = self.graphique.creer_frame(frame_high, bg='#cecece')
        self.message_label = tk.Label(self.root_frame, text="", fg="red")
        self.message_label.pack(padx=10, pady=10)

        def update_fonctionRand2(fonction):
            self.fonctionRand2 = fonction
            print("fonctionRand", self.fonctionRand2)

        # Boutons gauche
        self.bouton = self.graphique.creer_button(frame=self.frame_high_left, fonction=lambda: self.import_file(self.fonctionRand2), label="Importation d'un fichier")
        self.bouton.pack(padx=5, pady=5, side="left")
        self.bouton3 = self.graphique.creer_button(frame=self.frame_high_left, fonction=lambda: self.play_sequence("pirate.txt", self.fonctionRand2), label="RUN MUSIC")
        self.bouton3.pack(padx=5, pady=5, side="left")
        self.bouton4 = self.graphique.creer_button(frame=self.frame_high_left, fonction=lambda: self.stop_music(), label="STOP MUSIC")
        self.bouton4.pack(padx=5, pady=5, side="left")

        choix2  = tk.StringVar()
        choix2.set(60)  # Valeur par défaut

        self.boutonRadio5 = self.graphique.creer_radiobutton(frame=self.frame_high_left, variable=choix2, value=60, label="Lent", command=lambda: update_fonctionRand2(choix2.get()))
        self.boutonRadio5.pack(padx=5, pady=5, side="left")
        self.boutonRadio6 = self.graphique.creer_radiobutton(frame=self.frame_high_left, variable=choix2, value=90, label="Normal", command=lambda: update_fonctionRand2(choix2.get()))
        self.boutonRadio6.pack(padx=5, pady=5, side="left")
        self.boutonRadio7 = self.graphique.creer_radiobutton(frame=self.frame_high_left, variable=choix2, value=120, label="Rapide", command=lambda: update_fonctionRand2(choix2.get()))
        self.boutonRadio7.pack(padx=5, pady=5, side="left")


        

        def update_fonctionRand(fonction):
            self.fonctionRand = fonction
            print("fonctionRand", self.fonctionRand)
        # Boutons droite
        self.bouton2 = self.graphique.creer_button(frame=self.frame_high_right, fonction=lambda: self.read_random_sequence(self.fonctionRand), label="Lecture Séquence Aléatoire")
        self.bouton2.pack(padx=5, pady=5, side="left")
        
        # ajouter 4 radios dans le self.frame_high_right

        choix  = tk.StringVar()
        choix.set(60)  # Valeur par défaut

        self.entre = tk.Entry(self.frame_high_right, width=30)
        self.entre.pack(side="left", padx=5, pady=5)# On met le focus sur le champ de saisiself.entre.focus_set()print(self.entre.get())

        self.boutonRadio1 = self.graphique.creer_radiobutton(frame=self.frame_high_right, variable=choix, value=60, label="Lent", command=lambda: update_fonctionRand(choix.get()))
        self.boutonRadio1.pack(padx=5, pady=5, side="left")
        self.boutonRadio2 = self.graphique.creer_radiobutton(frame=self.frame_high_right, variable=choix, value=90, label="Normal", command=lambda: update_fonctionRand(choix.get()))
        self.boutonRadio2.pack(padx=5, pady=5, side="left")
        self.boutonRadio3 = self.graphique.creer_radiobutton(frame=self.frame_high_right, variable=choix, value=120, label="Rapide", command=lambda: update_fonctionRand(choix.get()))
        self.boutonRadio3.pack(padx=5, pady=5, side="left")
        self.boutonRadio4 = self.graphique.creer_radiobutton(frame=self.frame_high_right, variable=choix, value="Aléatoire", label="Aléatoire", command=lambda: update_fonctionRand(choix.get()))
        self.boutonRadio4.pack(padx=5, pady=5, side="left")



        self.boutonStop = self.graphique.creer_button(frame=self.frame_high_right, fonction=lambda: self.stop_music(), label="STOP MUSIC")
        self.boutonStop.pack(padx=5, pady=5, side="left")

        frame_high.pack(fill="both", expand=True)

        # Frame aside avec des boutons pour les instruments
        frame_aside = self.graphique.creer_frame(self.root_frame, bg="#FF0000")
        for i in range(1, 9):
            self.graphique.creer_button(frame=frame_aside, fonction=self.on_key_press, label=f"I{i}").pack(padx=5, pady=5, side="left")
        frame_aside.pack(fill="both", expand=True)

        # Piano
        self.clavier = Clavier(graphique=self.graphique, fenetre=frame_middle, canvas=self.canvas, largeur=50,
                               hauteur=150, top_margin=40, type='', left_margin=350)

        # Pour afficher le piano
        frame_middle.pack(side='top', fill="x", expand=True)

        self.frame_high_left.pack(side="left", fill="both", expand=True)
        self.frame_high_right.pack(side="right", fill="both", expand=True)

        self.fenetre_principale.bind("<Key>", self.on_key_press)

    def import_file(self, tempo):
        """Methode qui charge le fichier et qui joue les notes qui sont dedans"""

        file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
        if file_path:
            if not file_path.lower().endswith(".txt"):
                self.message_label.config(text="Veuillez sélectionner un fichier au format .txt")
                return
            self.load_music_file(file_path, tempo)

    def read_random_sequence(self,tempo):
        """
        Fonction qui génère une séquence aléatoire et la joue en fonction du tempo saisi.
        """
        # Récupérer la valeur de `self.entre` ici
        nb_de_notes_str = self.entre.get().strip()
        if not nb_de_notes_str:
            self.message_label.config(text="Veuillez entrer un tempo valide.")
            return

        try:
            nb_de_notes = int(nb_de_notes_str)
            if nb_de_notes <= 0:
                self.message_label.config(text="Le tempo doit être un nombre positif.")
                return
        except ValueError:
            self.message_label.config(text="Veuillez entrer un nombre valide pour le tempo.")
            return

        # Générer une séquence aléatoire de notes et jouer la séquence
        print(f"Lecture de la séquence aléatoire avec un tempo de : {nb_de_notes}")
        if tempo != None :
            mp.generate_random_sequence(self, nb_de_notes * 2, "test.txt", tempo)
            self.play_sequence("test.txt", 1)

    def load_music_file(self, file_path, tempo):
        self.message_label.config(text="")
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            if not lines:
                self.message_label.config(text="Le fichier est vide. Veuillez fournir un fichier valide.")
                return

            note_pattern = re.compile(r"^[A-Ga-g](#|b)?\d$")
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

                if note != "0" and note != "Unknown" and not note_pattern.match(note):
                    self.message_label.config(text=f"Note invalide à la ligne {line_number} : {note}")
                    return

            self.message_label.config(text=f"Fichier {file_path} importé avec succès")

        except Exception as e:
            self.message_label.config(text=f"Erreur lors de l'importation du fichier : {e}")

        # message = f"Choisissez la vitesse : \n la vitesse doit être comprise entre 0.5 à 3."
        #
        # title = "Choix de la vitesse"
        #
        # # On ouvre une dialog qui permet la saisie pour demander la vitesse qu'il veut utiliser pour jouer
        # dialog = Dialog(self.graphique, self.fenetre_principale, title, message, afficher_saisi=True)
        #
        # # On attend que la fenêtre se ferme
        # self.fenetre_principale.wait_window(dialog.get_fenetre())
        #
        # # On récupère la saisie
        # vitesse_saisie = dialog.get_saisis()
        #
        # if vitesse_saisie:
        #     vitesse_saisie = int(vitesse_saisie)
        #     if 0.5 > vitesse_saisie > 3:
        #         print("Veuillez choisir un nombre compris entre 0.5 et 3")
        #         self.action_avancer()
        #         return

        # Jouer la séquence de musique après l'importation
        self.play_sequence(file_path, tempo)

    def action_avancer(self):
        message = f"Choisissez la vitesse : \n la vitesse doit être comprise entre 0.5 à 3."

        title = "Choix de la vitesse"

        # On ouvre une dialog qui permet la saisie pour demander la vitesse qu'il veut utiliser pour jouer
        dialog = Dialog(self.graphique, self.fenetre_principale, title, message, afficher_saisi=True)

        # On attend que la fenêtre se ferme
        self.fenetre_principale.wait_window(dialog.get_fenetre())

        # On récupère la saisie
        vitesse_saisie = dialog.get_saisis()

        if vitesse_saisie:
            vitesse_saisie = int(vitesse_saisie)
            if vitesse_saisie < 0.5:
                print("Veuillez choisir un nombre compris entre 0.5 et 3")
                self.action_avancer()
                return

    def on_key_press(self, event):
        note = self.notes_clavier.get(event.char, None)

        if note:
            frequency = note_to_frequency.get(note, None)
            if frequency:
                self.play(frequency, 0.125)

                # On récupère l'id de la touche(lettre entrée)
                touche_id = self.clavier.touches.get(event.char, None)
                if touche_id:
                    # On récupère la couleur du bg de la touche entrée
                    current_fill = self.canvas.itemcget(touche_id, 'fill')

                    if current_fill == "white":
                        self.canvas.itemconfig(touche_id, fill="yellow")
                        self.fenetre_principale.after(150, lambda: self.canvas.itemconfig(touche_id, fill="white"))

                    elif current_fill == "black":
                        self.canvas.itemconfig(touche_id, fill="orange")
                        self.fenetre_principale.after(150, lambda: self.canvas.itemconfig(touche_id, fill="black"))

    def afficher(self):
        self.graphique.ouvrir_fenetre(self.fenetre_principale)
