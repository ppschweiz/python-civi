# Python-Civi tool for sending bills and voting material

The tool can do the following:
* Send regular bills and payment reminders to members in an automated fashion
* Send voting materials for the postal voting

Input data for the tool is primarily the CiviCRM member database. Member data is also updated in the CiviCRM as needed.

Output are mails and postal mail uploads to pingen.com.

## Needed variables

The following variables must be defined for the tool to work.

### CiviCRM member database credentials

`CIVI_API_URL` is the URL of the CiviCRM rest API.

`CIVI_SITE_KEY` is part of the CiviCRM access credential.

`CIVI_API_KEY` is part of the CiviCRM access credential.

### Mail server credentials

`SMTP_SERVER_ADDRESS` is the host adress of the SMTP server.

`SMTP_SERVER_PORT` is the port of the SMTP server.

`SMTP_USERNAME` is the login user name at the SMTP server.

`SMTP_PASSWORD` is the login password at the SMTP server.

### Notification settings

`ADMIN_MAIL_ADDRESS` is the mail address where an admin is notified of problems.

`STATS_MAIL_ADDRESS` is the mail address where weekly statistics are sent.

### Paylink API credentials (Bitpay, credit card)

`PAYLINK_BASE` is the URL on the main website where the payment can be made.

`PAYLINK_SECRET` is the secret used to authenticate payments from a member.

### External service providers

`PINGEN_TOKEN` is the pingen.com API secret used to send postal letters.

`POSTAL_SPEED`is the speed (and cost) to send postal mail (A-Post = 1, B-Post = 2)

### Specific for voting

`BULLETIN_SECRET` is the secret used to compute the security code on each voter card.

`VOTING_SENDER_PGP_KEY` is OpenPGP/gnupg public key ID of the PPV for votings.

`PPV_ID` is the member ID of the PPV who does not get to vote because he decided when the voting is tied.

### Specific for sending bills

`MEMBERS_SENDER_PGP_KEY` is OpenPGP/gnupg public key ID of the member administrations for bills.

### Test specific settings

`TESTBOX_NAME` is the fullname of the tester to send test mails.

`TESTBOX_MAIL` is the mail address to send test mails.

