from librairie.graphique.graphique_interface_tk import GraphiqueInterfaceTk
from ecran.ecran_menu import EcranPrincipale
from enums.ecran_etat_enum import EcranEtat
from ecran.getsionnaire_etat_ecran import GestionnaireEtatEcran

from note_frequence_base import note_to_frequency



if __name__ == "__main__":
    graphic = GraphiqueInterfaceTk()
    
    gestionnaire_etat_ecran = GestionnaireEtatEcran()

    ecran_principale = EcranPrincipale(graphic, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.PRINCIPAL, ecran_principale)

    ecran_principale.play(note_to_frequency["F7"], 1)
    ecran_principale.play(note_to_frequency["B3"], 4)
    ecran_principale.play(note_to_frequency["E5"], 0.5)

    gestionnaire_etat_ecran.afficher_etat()
