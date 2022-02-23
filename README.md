# JWT decode script

Python script which decodes a JWT.

## Requirements

* python 3.8
* PyJWT

## Usage

### Reading token claim

If you want to read the token claim without validation run the script with

```
$ python JWTdecode.py <token>
```

### Validate the token

If you want to validate the token (i.e. signature, audience and temporal validity) run the script with

```
$ python JWTdecode.py -v <token>
```

Further options are:

* `-a audience` to set the expected audience. Default is "https://wlcg.cern.ch/jwt/v1/any"
* `-k jwkUrl` URL of the public RSA signing key. Default is "https://wlcg.cloud.cnaf.infn.it/jwk"

Run `python JWTdecode.py -h` for help page.