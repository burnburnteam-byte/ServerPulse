# Bot Discord pour lancer un serveur Aternos

Commandes : `/start`, `/stop`, `/status`

## Variables à créer sur Railway (onglet Variables)

| Nom | Valeur |
|---|---|
| DISCORD_TOKEN | token du bot Discord |
| ATERNOS_USER | pseudo Aternos |
| ATERNOS_PASS | mot de passe Aternos |
| ALLOWED_ROLE_ID | (optionnel) ID du rôle autorisé, sinon tout le monde |
| ATERNOS_SESSION | (optionnel) cookie ATERNOS_SESSION si Cloudflare bloque le login |

Ne jamais mettre de token ou de mot de passe dans les fichiers.

## Test en local (PowerShell, Python 3.11)

    py -3.11 -m pip install -r requirements.txt
    $env:DISCORD_TOKEN="..."
    $env:ATERNOS_USER="..."
    $env:ATERNOS_PASS="..."
    py -3.11 bot.py
