import jwt
from jwt import PyJWKClient
from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import InvalidAudienceError
import json 
import argparse

def command_line_parser():

	parser = argparse.ArgumentParser()
	
	parser.add_argument("token", help="JWT to be decoded")
	
	parser.add_argument("-a", "--audience", 
		default="https://wlcg.cern.ch/jwt/v1/any", 
		help="JWT audience claim.\
		Default to 'https://wlcg.cern.ch/jwt/v1/any'")
		
	parser.add_argument("-k" ,"--jwkUrl", 
		default="https://wlcg.cloud.cnaf.infn.it/jwk",
		help="URL of the public RSA signing key")
		
	parser.add_argument("-v", "--verify",
		action="store_true",
		help="verify token: signature, temporal validity and audience.\
		Set proper audience with '-a' option if different from default.")
		
	args = parser.parse_args()
	
	return args

def decode_JWT(token):
	
	data = jwt.decode(token, options={"verify_signature": False})
	
	return data

def verify_JWT(jwkUrl, token, audience):

	jwks_client = PyJWKClient(jwkUrl)
	signing_key = jwks_client.get_signing_key_from_jwt(token)
	key = signing_key.key

	header_data = jwt.get_unverified_header(token)
	payload_data = decode_JWT(token)

	if payload_data.get('aud') != None:
		data = jwt.decode(token, key, algorithms=[header_data['alg']], 
			options={"verify_exp": True}, audience=audience)
	else: 
		data = jwt.decode(token, key, algorithms=[header_data['alg']], 
			options={"verify_exp": True})
	
	return data

def main():

	args = command_line_parser()
	token = args.token
	jwkUrl = args.jwkUrl
	audience = args.audience
	
	try:
		if args.verify:
			decoded_JWT = verify_JWT(jwkUrl, token, audience)
		else:
			decoded_JWT = decode_JWT(token)
			
		print(json.dumps(decoded_JWT, indent = 2))

	except (ExpiredSignatureError, InvalidAudienceError) as error:
		print(f'Unable to decode the token, error: {error}')
	

if __name__ == "__main__":
    main()

