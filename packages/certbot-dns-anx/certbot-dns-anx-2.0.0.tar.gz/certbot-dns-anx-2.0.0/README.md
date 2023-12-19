ANX DNS Authenticator for Certbot
=================================
This allows automatic completion of [Certbot's](https://github.com/certbot/certbot)
DNS01 challange for domains managed on [ANX DNS](https://dyn.anx.se/api/dns/)

Important information
---------------------
PLEASE NOTE THAT ONE OF THE DEPENDENCIES TO THE LIBRARY INCLUDED A BAD INSTALL_REQUIRES.


Installing
----------
```
   $ pip install certbot-anx
```
   
Usage
-----
The plugin requires a API key that is created here: http://dyn.anx.se/users/users.jsf?i=2

To use the authenticator you need to provide some required options:

``--certbot-anx:credentials`` *(required)*
  ANX API credentials INI file. (default: None)

The credentials file must have the folling format:

```
   certbot_anx:api_key = codegoeshere
```
For safety reasons the file must not be world readable. You can solve this by
running:

```
   $ chmod 600 credentials.ini
```
Then you can run ``certbot`` using:

```
    $ sudo certbot certonly \
        --authenticator certbot-anx:auth \
        --certbot-anx:auth-credentials credentials.ini \
        -d domain.com
```
If you want to obtain a wildcard certificate you can use the
``--server https://acme-v02.api.letsencrypt.org/directory`` flag and the domain
``-d *.domain.com``
