from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran


class GestionnaireEtatEcran:
    def __init__(self):
        """
        Initialise la classe GestionnaireEtatEcran et par défaut c'est l'écran du menu qui est affiché.
        ----------------------------------------------------------

        """
        self.etat: EcranEtat = EcranEtat.PRINCIPAL
        self.ecrans = {}

    def ajouter_ecran(self, etat: EcranEtat, ecran: Ecran):
        """
        Ajoute un écran.
        ----------------------------------------------------------

        Args:
            graphique (GraphiqueInterface) : l'instance de la classe Graphique
            gestionnaire_etat_ecran (GestionnaireEtatEcran) : l'instance de la classe GestionnaireEtatEcran

        """
        self.ecrans[etat] = ecran

    def get_etat(self):
        return self.etat

    def set_etat(self, etat: EcranEtat):
        self.etat = etat

    def afficher_etat(self):
        """
        Affiche l'écran qui correspond à l'état actuel.
        ----------------------------------------------------------

        """
        view = self.ecrans.get(self.get_etat())
        view.initialiser_interface()
        view.afficher()
