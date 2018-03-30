#!/bin/bash

# CiviCRM member database credentials
export CIVI_API_URL="https://members-crm.piratenpartei.ch/wp-content/plugins/civicrm/civicrm/extern/rest.php"
export CIVI_SITE_KEY="secret!"
export CIVI_API_KEY="secret!"

# Cyon mail server credentials
export SMTP_SERVER_ADDRESS="mail.cyon.ch"
export SMTP_SERVER_PORT="587"
export SMTP_USERNAME="givenname.surname@piratenpartei.ch"
export SMTP_PASSWORD="secret!"

# Mail address where an admin is notified of problems
export ADMIN_MAIL_ADDRESS="givenname.surname@piratenpartei.ch"

# Paylink API credentials (Bitpay, credit card)
export PAYLINK_BASE="https://www.piratenpartei.ch"
export PAYLINK_SECRET="secret!"

# Pingen.com API credentials for send postal letters
export PINGEN_TOKEN="secret!"

# Secret for the voting security codes
export BULLETIN_SECRET="secret!"

# OpenPGP/gnupg public key ID of the PPV for votings
export VOTING_SENDER_PGP_KEY="2B18DEF9EA6310DB"

# OpenPGP/gnupg public key ID of the members OTRS for bills
export MEMBERS_SENDER_PGP_KEY="BC0DB1E1CE74C0A9"

# Member ID of the PPV who does not get to vote because he decided when the voting is tied
export PPV_ID="553"

# Speed to send postal mail (A-Post = 1, B-Post = 2)
export POSTAL_SPEED="1"

# Where any test mails go
export TESTBOX_NAME="Stefan Thöni"
export TESTBOX_MAIL="stefan.thoeni@piratenpartei.ch"

