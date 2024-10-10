import numpy as np
import pygame
from note_frequence_base import note_to_frequency

class MusicPlayer:
    def __init__(self, sample_rate=44100):
        pygame.mixer.init(frequency=sample_rate, size=-16, channels=2)
        self.sample_rate = sample_rate

    def apply_adsr_envelope(self, tone, attack, decay, sustain_level, release, duration):
        total_samples = int(self.sample_rate * duration)
        envelope = np.zeros(total_samples)

        # Attack
        attack_samples = int(self.sample_rate * attack)
        if attack_samples > total_samples:
            attack_samples = total_samples

        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

        # Decay
        decay_samples = int(self.sample_rate * decay)
        if attack_samples + decay_samples > total_samples:
            decay_samples = total_samples - attack_samples

        envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain_level, decay_samples)

        # Sustain
        sustain_samples = total_samples - (attack_samples + decay_samples + int(self.sample_rate * release))
        if sustain_samples < 0:
            sustain_samples = 0

        envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = sustain_level

        # Release
        release_samples = int(self.sample_rate * release)
        if release_samples > total_samples - (attack_samples + decay_samples + sustain_samples):
            release_samples = total_samples - (attack_samples + decay_samples + sustain_samples)

        envelope[total_samples - release_samples:] = np.linspace(sustain_level, 0, release_samples)

        return tone * envelope


    def play_piano_tone(self, frequency, duration):

        print("duration", duration)
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)

        # Synthèse additive avec plusieurs harmoniques pour imiter le son d'un piano
        tone = (0.5 * np.sin(frequency * 2 * np.pi * t) +                    # Fondamentale
                0.25 * np.sin(2 * frequency * 2 * np.pi * t) +              # 1ère harmonique
                0.125 * np.sin(3 * frequency * 2 * np.pi * t) +             # 2ème harmonique
                0.1 * np.sin(4 * frequency * 2 * np.pi * t) +                # 3ème harmonique
                0.05 * np.sin(5 * frequency * 2 * np.pi * t))                # 4ème harmonique

        # Appliquer l'enveloppe ADSR
        tone_with_adsr = self.apply_adsr_envelope(tone, attack=0.02, decay=0.1, sustain_level=0.5, release=0.2, duration=duration)

        # Convertir en format audio
        stereo_tone = np.vstack((tone_with_adsr, tone_with_adsr)).T
        contiguous_tone = np.ascontiguousarray((32767 * stereo_tone).astype(np.int16))

        sound = pygame.sndarray.make_sound(contiguous_tone)
        sound.set_volume(0.05)  # Réglez le volume
        sound.play()
        pygame.time.delay(int(duration * 1000))

    # lecture d'un fichier texte contenant une séquence de notes
    def play_sequence(self, filename):
        notes_sequence = []
        duration_sequence = []

        with open(filename, "r") as f:
            for line in f:
                note = line.split()[0]
                duration = float(line.split()[1])
                notes_sequence.append(note)
                duration_sequence.append(duration)


        for note, duration in zip(notes_sequence, duration_sequence):

            # print(note, duration)

            if (note == "Unknown"):
                continue

            if (note == "0"):
                pygame.time.delay(int(duration * 1000))
                continue

            frequency = note_to_frequency[note]
            self.play_piano_tone(frequency, duration)



# Code pour jouer la suite de notes
if __name__ == "__main__":
    mp = MusicPlayer()
    mp.play_sequence("pirate.txt")
