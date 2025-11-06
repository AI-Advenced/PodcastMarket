# PodcastMarket 🎙️

Marketplace de publicité podcast connectant les marques avec les podcasters pour du contenu sponsorisé et des publicités lues par l'hôte.

## 🚀 Production

<img width="1538" height="827" alt="image" src="https://github.com/user-attachments/assets/a94f1dbc-c706-46f9-84d4-0e01f46ea177" />



## 📋 Aperçu du Projet

PodcastMarket est une plateforme marketplace complète qui permet :
- **Pour les Podcasters** : Monétiser leur audience en acceptant des publicités ciblées
- **Pour les Marques** : Trouver les podcasts pertinents pour leur audience et gérer leurs campagnes
- **Négociation** : Système de négociation intégré pour des accords gagnant-gagnant
- **Tracking** : Suivi des performances avec analytics détaillés (impressions, conversions, ROI)

## ✨ Fonctionnalités Complétées

### 🔐 Authentification
- ✅ Inscription utilisateur (Podcaster / Marque)
- ✅ Connexion/Déconnexion
- ✅ Gestion de profil utilisateur
- ✅ Validation des emails et mots de passe

### 🎙️ Gestion des Podcasts
- ✅ Création et édition de podcasts
- ✅ Informations détaillées (catégorie, audience, tarifs)
- ✅ Liens vers Apple Podcasts, Spotify, RSS feed
- ✅ Marketplace de podcasts avec recherche et filtres
- ✅ Page de détails avec métriques d'audience

### 🏢 Gestion des Marques
- ✅ Création et édition de profils marque
- ✅ Informations entreprise (industrie, budget mensuel)
- ✅ Gestion des préférences de ciblage

### 📢 Système de Campagnes
- ✅ Création de campagnes publicitaires
- ✅ Types d'annonces : pre-roll, mid-roll, post-roll, host-read
- ✅ Gestion du budget et des tarifs
- ✅ Approbation de contenu
- ✅ États de campagne : draft, pending, negotiating, approved, active, completed, cancelled

### 🤝 Négociation (Deals)
- ✅ Système d'offres et contre-offres
- ✅ Historique complet des négociations
- ✅ Acceptation/Rejet des offres
- ✅ Mise à jour automatique des tarifs négociés

### 📊 Tracking & Analytics
- ✅ Suivi des performances par épisode
- ✅ Métriques détaillées :
  - Impressions et auditeurs uniques
  - Click-through rate (CTR)
  - Utilisations de codes promo
  - Conversions
  - Revenus générés
- ✅ Calcul automatique du ROI
- ✅ Analytics par campagne, podcast et marque
- ✅ Dashboards personnalisés (Podcaster vs Marque)

### 🎨 Interface Utilisateur
- ✅ Design moderne avec TailwindCSS
- ✅ Navigation responsive
- ✅ Pages de marketplace élégantes
- ✅ Formulaires intuitifs
- ✅ Messages flash pour feedback utilisateur
- ✅ Icons FontAwesome

## 🛠️ Stack Technique

### Backend
- **Framework** : Flask 3.0.0
- **ORM** : Flask-SQLAlchemy 3.1.1
- **Base de données** : SQLite (podcastmarket.db)
- **Auth** : Flask-Login 0.6.3
- **Migrations** : Flask-Migrate 4.0.5

### Frontend
- **CSS Framework** : TailwindCSS (CDN)
- **Icons** : FontAwesome 6.4.0
- **HTTP Client** : Axios 1.6.0
- **Fonts** : Google Fonts (Inter)

### Déploiement
- **Process Manager** : PM2
- **Python Version** : 3.x
- **Port** : 3000

## 📊 Modèles de Données

### User
- Authentification (email, username, password)
- Type d'utilisateur : `podcast_host` ou `brand`
- Profil (nom complet, entreprise, bio, avatar, website)
- Statut (actif, vérifié)

### Podcast
- Informations de base (titre, description, cover image)
- Catégorie et langue
- Métriques d'audience (auditeurs moyens, nombre d'épisodes)
- Tarifs (min_rate, max_rate)
- Liens externes (RSS, Apple Podcasts, Spotify)

### Brand
- Informations entreprise (nom, logo, industrie, taille)
- Budget (mensuel, total dépensé)
- Ciblage (démographiques, catégories préférées)

### Campaign
- Détails campagne (titre, description, type d'annonce)
- Timing (dates début/fin, nombre d'épisodes)
- Financier (tarif proposé, tarif négocié, budget total)
- Contenu (script, code promo, URL tracking)
- Statut et approbation

### Deal
- Offres de négociation
- Historique des contre-offres
- Statut des réponses (pending, accepted, rejected, countered)

### AdPerformance
- Métriques par épisode
- Impressions, clics, conversions
- Revenus générés
- Calculs ROI, CTR, taux de conversion

## 📁 Structure du Projet

```
webapp/
├── app/
│   ├── __init__.py              # Factory pattern Flask
│   ├── models/                  # Modèles SQLAlchemy
│   │   ├── user.py
│   │   ├── podcast.py
│   │   ├── brand.py
│   │   ├── campaign.py
│   │   ├── deal.py
│   │   └── tracking.py
│   ├── routes/                  # Blueprints Flask
│   │   ├── auth.py             # Authentification
│   │   ├── main.py             # Pages principales
│   │   ├── podcasts.py         # Gestion podcasts
│   │   ├── brands.py           # Gestion marques
│   │   ├── campaigns.py        # Gestion campagnes
│   │   ├── deals.py            # Négociations
│   │   └── analytics.py        # Analytics
│   ├── templates/               # Templates Jinja2
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── marketplace.html
│   │   └── auth/
│   └── static/                  # Fichiers statiques
├── config.py                    # Configuration Flask
├── run.py                       # Point d'entrée
├── requirements.txt             # Dépendances Python
├── ecosystem.config.cjs         # Configuration PM2
├── .env                         # Variables d'environnement
├── .gitignore                   # Git ignore
└── podcastmarket.db             # Base SQLite
```

## 🎯 URIs et Routes Principales

### Pages Publiques
- `GET /` - Page d'accueil
- `GET /marketplace` - Marketplace des podcasts
- `GET /about` - À propos

### Authentification
- `GET/POST /auth/register` - Inscription
- `GET/POST /auth/login` - Connexion
- `GET /auth/logout` - Déconnexion
- `GET /auth/profile` - Profil utilisateur
- `POST /auth/profile/update` - Mise à jour profil

### Dashboard
- `GET /dashboard` - Dashboard personnalisé (Podcaster/Marque)
- `GET /api/stats` - Statistiques utilisateur (API JSON)

### Podcasts
- `GET /podcasts/` - Liste des podcasts
- `GET /podcasts/<id>` - Détails podcast
- `GET/POST /podcasts/create` - Créer un podcast
- `GET/POST /podcasts/<id>/edit` - Éditer podcast
- `POST /podcasts/<id>/delete` - Supprimer podcast
- `GET /podcasts/my` - Mes podcasts

### Marques
- `GET /brands/` - Liste des marques
- `GET /brands/<id>` - Détails marque
- `GET/POST /brands/create` - Créer une marque
- `GET/POST /brands/<id>/edit` - Éditer marque
- `POST /brands/<id>/delete` - Supprimer marque
- `GET /brands/my` - Mes marques

### Campagnes
- `GET /campaigns/` - Mes campagnes
- `GET /campaigns/<id>` - Détails campagne
- `GET/POST /campaigns/create` - Créer campagne
- `POST /campaigns/<id>/update-status` - Mettre à jour statut
- `POST /campaigns/<id>/approve-content` - Approuver contenu
- `POST /campaigns/<id>/complete` - Marquer comme terminée

### Négociations
- `GET /deals/campaign/<campaign_id>` - Historique des négociations
- `POST /deals/create` - Créer une offre
- `POST /deals/<id>/respond` - Répondre à une offre
- `GET /deals/<id>` - Détails d'une négociation

### Analytics
- `GET /analytics/campaign/<id>` - Analytics campagne
- `GET /analytics/podcast/<id>` - Analytics podcast
- `GET /analytics/brand/<id>` - Analytics marque
- `POST /analytics/performance/add` - Ajouter données performance

## 🔧 Installation et Démarrage

### Prérequis
- Python 3.8+
- pip3
- PM2 (pré-installé dans le sandbox)

### Installation

```bash
# Cloner le repository
cd /home/user/webapp

# Installer les dépendances
pip3 install -r requirements.txt

# Initialiser la base de données
flask init-db

# Seed avec des données de test
flask seed-db
```

### Démarrage

```bash
# Nettoyer le port (si nécessaire)
fuser -k 3000/tcp 2>/dev/null || true

# Démarrer avec PM2
pm2 start ecosystem.config.cjs

# Vérifier le statut
pm2 list

# Voir les logs
pm2 logs podcastmarket --nostream
```

## 👥 Comptes de Test

### Podcaster
- **Email** : podcast@example.com
- **Password** : password123
- **Type** : Podcast Host

### Marque
- **Email** : brand@example.com
- **Password** : password123
- **Type** : Brand

## 🚀 Fonctionnalités Non Implémentées (Recommandations)

### Priorité Haute
1. **Upload d'images** - Cover podcast et logos marques
2. **Notifications email** - Alertes pour nouvelles offres/réponses
3. **Système de paiement** - Intégration Stripe pour paiements automatisés
4. **Recherche avancée** - Filtres par audience, budget, catégories multiples
5. **Templates de profil** - Profils publics pour podcasts et marques

### Priorité Moyenne
6. **Export PDF** - Contrats et rapports analytics
7. **Messagerie interne** - Communication directe entre parties
8. **Calendrier de publication** - Planning des épisodes sponsorisés
9. **API REST** - Documentation Swagger/OpenAPI
10. **Tests automatisés** - Tests unitaires et d'intégration

### Priorité Basse
11. **Multi-langue** - Support i18n (actuellement français uniquement)
12. **Dark mode** - Thème sombre
13. **Recommandations IA** - Matching automatique podcast-marque
14. **Intégrations** - Google Analytics, Facebook Pixel
15. **Mobile app** - Application mobile native

## 📈 Prochaines Étapes Recommandées

1. **Upload d'images** :
   - Configurer upload de fichiers avec Flask
   - Stocker les images localement ou sur CDN
   - Valider formats et tailles d'images

2. **Système de notifications** :
   - Intégrer Flask-Mail
   - Templates email HTML
   - Notifications pour nouvelles campagnes, offres, approbations

3. **Paiements** :
   - Intégration Stripe ou PayPal
   - Gestion des transactions
   - Historique de paiements

4. **Tests** :
   - pytest pour tests unitaires
   - Tests des routes et modèles
   - Tests d'intégration

5. **Documentation API** :
   - Swagger/OpenAPI
   - Documentation des endpoints JSON

## 📝 Notes Techniques

### Base de Données
- SQLite pour développement (facile à déployer)
- Migrations Flask-Migrate pour évolution du schéma
- Pour production, migrer vers PostgreSQL recommandé

### Sécurité
- Mots de passe hashés avec Werkzeug
- Sessions sécurisées avec Flask-Login
- CSRF protection via Flask-WTF
- Validation des permissions sur chaque route

### Performance
- Index sur colonnes fréquemment recherchées
- Lazy loading pour relations SQLAlchemy
- Pagination recommandée pour grandes listes

### Déploiement Production
- Utiliser Gunicorn au lieu du serveur Flask dev
- Configurer Nginx comme reverse proxy
- Variables d'environnement pour secrets
- Sauvegardes régulières de la base de données

## 🤝 Contribution

Ce projet est un MVP (Minimum Viable Product). Les contributions sont bienvenues pour :
- Corriger des bugs
- Ajouter des fonctionnalités
- Améliorer la documentation
- Optimiser les performances

## 📄 Licence

Tous droits réservés © 2024 PodcastMarket

## 👨‍💻 Développé avec

- ❤️ Python + Flask
- 🎨 TailwindCSS
- 🗄️ SQLite
- ⚡ PM2

---

**Status** : ✅ En ligne et opérationnel  
**Dernière mise à jour** : 6 novembre 2025  
**Version** : 1.0.0 (MVP)
