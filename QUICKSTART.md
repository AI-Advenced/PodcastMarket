# 🚀 Guide de Démarrage Rapide - PodcastMarket

## 🌐 Accès Immédiat

**URL de l'Application** : https://3000-imbyy9gzpxu1h15byf03t-2b54fc91.sandbox.novita.ai

## 👥 Comptes de Test

### 🎙️ Compte Podcaster
```
Email: podcast@example.com
Mot de passe: password123
```
**Ce compte permet de** :
- Voir et créer des podcasts
- Recevoir des propositions de campagnes
- Négocier avec les marques
- Approuver/rejeter des campagnes
- Ajouter des données de performance

### 🏢 Compte Marque
```
Email: brand@example.com
Mot de passe: password123
```
**Ce compte permet de** :
- Créer des profils de marque
- Parcourir le marketplace de podcasts
- Créer des campagnes publicitaires
- Négocier avec les podcasters
- Voir les analytics de campagnes

## 🎯 Scénarios de Test

### Scénario 1 : Podcaster recevant une campagne (déjà configuré !)

1. **Connectez-vous en tant que Podcaster** (podcast@example.com)
2. Allez sur **Dashboard** - vous verrez :
   - 1 podcast existant : "Tech Talk France"
   - 1 campagne en attente : "TechCorp Product Launch"
3. Cliquez sur la campagne pour voir les détails
4. Actions possibles :
   - Approuver la campagne
   - Négocier le tarif
   - Rejeter la campagne

### Scénario 2 : Marque créant une nouvelle campagne

1. **Connectez-vous en tant que Marque** (brand@example.com)
2. Allez sur **Marketplace** pour voir les podcasts disponibles
3. Cliquez sur un podcast qui vous intéresse
4. Cliquez sur "Créer une campagne"
5. Remplissez le formulaire :
   - Sélectionnez votre marque
   - Type d'annonce (host-read recommandé)
   - Budget proposé
   - Dates et nombre d'épisodes
6. Soumettez et attendez la réponse du podcaster

### Scénario 3 : Négociation

1. **Podcaster** : Ouvrez la campagne en attente
2. Cliquez sur "Négocier" (bouton dans les deals/négociations)
3. Proposez un contre-tarif
4. **Marque** : Reconnectez-vous avec le compte marque
5. Voyez la contre-offre
6. Acceptez ou proposez un nouveau tarif

### Scénario 4 : Suivi des performances

1. **Podcaster** : Une fois la campagne approuvée et active
2. Allez dans Analytics → Campagne
3. Cliquez sur "Ajouter des données de performance"
4. Entrez :
   - Titre et numéro de l'épisode
   - Impressions (ex: 5000)
   - Clics (ex: 250)
   - Conversions (ex: 25)
   - Revenus générés (ex: 500€)
5. **Marque** : Voir les analytics mises à jour avec ROI calculé

## 📋 Parcours Utilisateur Complets

### Pour un Nouveau Podcaster

```
1. S'inscrire → Type: Podcast Host
2. Compléter le profil
3. Créer un podcast
   - Titre, description
   - Catégorie (Technology, Business, etc.)
   - Nombre d'auditeurs moyens
   - Tarifs min/max par épisode
   - Liens (Apple Podcasts, Spotify, RSS)
4. Attendre les propositions de marques
5. Négocier et approuver les campagnes
6. Enregistrer les épisodes sponsorisés
7. Suivre les performances
```

### Pour une Nouvelle Marque

```
1. S'inscrire → Type: Brand
2. Compléter le profil
3. Créer un profil de marque
   - Nom, logo, industrie
   - Budget mensuel
   - Audience cible
4. Explorer le marketplace
5. Filtrer par catégorie/audience
6. Créer une campagne
7. Négocier avec le podcaster
8. Approuver le contenu
9. Suivre les résultats (impressions, conversions, ROI)
```

## 🔍 Fonctionnalités à Tester

### ✅ Authentification
- [ ] Inscription nouveau compte
- [ ] Connexion
- [ ] Déconnexion
- [ ] Mise à jour de profil

### ✅ Podcasts
- [ ] Créer un podcast
- [ ] Éditer un podcast existant
- [ ] Voir le marketplace
- [ ] Rechercher par catégorie
- [ ] Voir les détails d'un podcast

### ✅ Marques
- [ ] Créer une marque
- [ ] Éditer une marque
- [ ] Voir ses marques

### ✅ Campagnes
- [ ] Créer une campagne
- [ ] Voir le statut d'une campagne
- [ ] Approuver/Rejeter une campagne (podcaster)
- [ ] Approuver le contenu (marque)
- [ ] Marquer comme terminée

### ✅ Négociations
- [ ] Faire une contre-offre
- [ ] Accepter une offre
- [ ] Rejeter une offre
- [ ] Voir l'historique des négociations

### ✅ Analytics
- [ ] Ajouter des données de performance
- [ ] Voir les analytics d'une campagne
- [ ] Voir les analytics d'un podcast
- [ ] Voir les analytics d'une marque
- [ ] Vérifier les calculs de ROI

## 🎨 Navigation Rapide

### Pages Principales
- **/** - Page d'accueil
- **/marketplace** - Parcourir les podcasts
- **/dashboard** - Dashboard personnalisé
- **/podcasts/my** - Mes podcasts (podcaster)
- **/brands/my** - Mes marques (marque)
- **/campaigns/** - Mes campagnes

### Actions Rapides
- **Podcaster** :
  - Dashboard → "Mes Podcasts" → "Créer un podcast"
  - Dashboard → Voir les campagnes en attente
  
- **Marque** :
  - Marketplace → Choisir un podcast → "Créer une campagne"
  - Dashboard → "Mes Marques" → "Créer une marque"

## 💡 Conseils de Test

1. **Testez les deux rôles** : Utilisez deux onglets de navigateur différents (un pour chaque compte)
2. **Négociez** : Le système de deals est le cœur de l'application
3. **Regardez les analytics** : Le calcul automatique du ROI est impressionnant
4. **Essayez les filtres** : La recherche dans le marketplace fonctionne bien
5. **Testez les validations** : Essayez de créer des campagnes avec des champs manquants

## 🐛 Que Faire en Cas de Problème ?

### L'application ne répond pas
```bash
# Redémarrer PM2
pm2 restart podcastmarket

# Vérifier les logs
pm2 logs podcastmarket --nostream
```

### Erreur de base de données
```bash
# Réinitialiser la DB
cd /home/user/webapp
rm podcastmarket.db
flask init-db
flask seed-db
pm2 restart podcastmarket
```

### Port déjà utilisé
```bash
fuser -k 3000/tcp
pm2 restart podcastmarket
```

## 📞 Support

Pour toute question ou bug :
1. Vérifiez les logs : `pm2 logs podcastmarket --nostream`
2. Consultez le README.md pour la documentation complète
3. Vérifiez que vous êtes bien connecté avec le bon compte (podcaster vs marque)

## 🎉 Amusez-vous bien !

PodcastMarket est une application complète avec toutes les fonctionnalités essentielles d'une marketplace. Explorez et testez tous les aspects du workflow podcaster-marque !

---

**URL** : https://3000-imbyy9gzpxu1h15byf03t-2b54fc91.sandbox.novita.ai  
**Version** : 1.0.0 MVP
