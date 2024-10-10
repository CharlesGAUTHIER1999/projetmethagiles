from librairie.graphique.graphique_interface_tk import GraphiqueInterfaceTk
from ecran.ecran_principal import EcranPrincipal
from enums.ecran_etat_enum import EcranEtat
from ecran.getsionnaire_etat_ecran import GestionnaireEtatEcran


if __name__ == "__main__":
    graphic = GraphiqueInterfaceTk()

    gestionnaire_etat_ecran = GestionnaireEtatEcran()

    ecran_principal = EcranPrincipal(graphic, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.PRINCIPAL, ecran_principal)

    gestionnaire_etat_ecran.afficher_etat()
