# Gestion de formation (console, Python)

Application console de gestion d'étudiants, de formateurs, de cours, d'inscriptions et d'évaluations, avec sauvegarde JSON.

**Participants :** _à compléter (noms de l'équipe)_

## Lancement

Python 3.10+ requis, aucune dépendance externe.

```bash
python main.py data/demo.json     # avec les données de démonstration
python main.py                    # fichier par défaut : data/formation.json (créé s'il est absent)
python generer_demo.py            # régénère data/demo.json
python -m unittest discover -s tests -v   # tests
```

## Structure

| Fichier | Rôle |
|---|---|
| `models.py` | Classes : `Personne` → `Etudiant` / `Formateur`, `Cours`, `Inscription`, `Evaluation`, `Creneau` |
| `service.py` | Règles métier (`Systeme`) : conflits, capacité, file d'attente, moyennes, statistiques |
| `storage.py` | Chargement / sauvegarde JSON |
| `main.py` | Menus console et tableaux de bord |

## Règles métier

- **Conflits d'horaires** : vérifiés avant toute inscription et toute assignation de formateur. Deux créneaux qui se touchent (10:00 fin / 10:00 début) ne sont pas en conflit.
- **Capacité** : cours plein → inscription « en attente ». Au désistement d'un étudiant confirmé, la place va au premier de la file qui n'a pas de conflit d'horaires.
- **Notes manquantes** : au choix, ignorées dans la moyenne (défaut) ou comptées 0 (menu Évaluations).
- **Moyenne** : somme(note × coefficient) / somme(coefficients).
- **Intégrité** : chaque opération est une transaction. Si elle échoue (règle violée ou erreur d'écriture), l'état est restauré, aucune modification partielle.

## Persistance

Sauvegarde automatique après chaque modification (écriture atomique via fichier temporaire). Fichier absent : créé. Fichier invalide ou incohérent : le programme refuse de démarrer **sans l'écraser**. Les identifiants (`E001`, `C002`…) restent uniques après redémarrage.
