"""Génère data/demo.json en passant par les vraies règles métier."""
from pathlib import Path

from models import Creneau as C
from storage import sauvegarder
from service import Systeme

CHEMIN = Path("data/demo.json")


def main():
    if CHEMIN.exists():
        CHEMIN.unlink()
    s = Systeme(persister=lambda sys_: sauvegarder(sys_, CHEMIN))

    f1 = s.ajouter_formateur("Martin", "Claire", "claire.martin@ecole.fr", "Informatique")
    f2 = s.ajouter_formateur("Durand", "Paul", "paul.durand@ecole.fr", "Électronique")

    e = [s.ajouter_etudiant(n, p, f"{p.lower()}.{n.lower()}@etu.fr", "Génie électrique")
         for n, p in [("Bernard", "Alice"), ("Petit", "Hugo"), ("Moreau", "Lina"),
                      ("Roux", "Yanis"), ("Fournier", "Emma"), ("Girard", "Noé")]]

    c1 = s.creer_cours("Programmation Python", 3,
                       [C("lundi", "08:00", "10:00"), C("mercredi", "14:00", "16:00")], f1)
    c2 = s.creer_cours("Algèbre linéaire", 2, [C("mardi", "10:00", "12:00")], f2)
    c3 = s.creer_cours("Électronique analogique", 3, [C("lundi", "09:00", "11:00")], f2)

    # Programmation : 3 places, 4 candidats -> le 4e en file d'attente
    for etu in e[:4]:
        s.inscrire(etu, c1)
    # Algèbre : 2 places, E001 + E002 confirmés, E003 en attente
    s.inscrire(e[0], c2)
    s.inscrire(e[1], c2)
    s.inscrire(e[2], c2)
    # Électronique : E005 et E006 (E001 aurait un conflit avec Programmation le lundi)
    s.inscrire(e[4], c3)
    s.inscrire(e[5], c3)

    # Désistement de E002 en Algèbre -> E003 passe automatiquement de la file à confirmé
    insc = next(i for i in s.inscriptions.values() if i.etudiant_id == e[1] and i.cours_id == c2)
    s.desister(insc.id)

    # Évaluations et notes (E003 n'a pas de note à l'examen : cas « note manquante »)
    tp1 = s.creer_evaluation(c1, "TP1", 1)
    exam = s.creer_evaluation(c1, "Examen", 2)
    ds1 = s.creer_evaluation(c2, "DS1", 1)
    for etu, n1, n2 in [(e[0], 14, 16), (e[1], 8, 9)]:
        s.saisir_note(tp1, etu, n1)
        s.saisir_note(exam, etu, n2)
    s.saisir_note(tp1, e[2], 12)
    s.saisir_note(ds1, e[0], 11)
    s.saisir_note(ds1, e[2], 7)
    print(f"Démo générée : {CHEMIN}")


if __name__ == "__main__":
    main()
