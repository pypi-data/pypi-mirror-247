# pylint: disable=no-name-in-module

"""Helper functions for the authentication process."""

import base64
import hashlib
import hmac
import json
import re
from json.decoder import JSONDecodeError
from typing import Any, Dict, Match, Optional, Tuple, Union, cast

import jwt
import requests

from multiauth.entities.errors import AuthenticationError
from multiauth.entities.main import AuthHashAlgorithmDigest, AuthResponse, AuthTech, JWTToken, Token
from multiauth.entities.providers.oauth import AuthOAuthlocation
from multiauth.utils import dict_nested_get


def extract_token(
    response: requests.Response,
    tech: AuthTech,
    headers: Dict[str, str],
    refresh_token_name: Optional[str] = None,
) -> Tuple[AuthResponse, Optional[str]]:
    """This function takes the response and tries to extract the tokens.

    This function is mainly a helper function to the REST and the GraphQL authenctication schema.
    The goal of the function is to generate the authentication
    response according to the extracted tokens from the repsonse
    """

    def _find_token(token: Any, response: Any) -> Any:
        """This function finds the value of the token."""
        result = response

        if len(token) > 0:
            token_name = token[0]
            res_token_name: Any = dict_nested_get(result, token_name)
            result = _find_token(token[1:], res_token_name)

        return result

    if response.status_code is None or response.status_code >= 400:
        raise AuthenticationError(f'Response returned for authentication has failed: {response.text}')

    try:
        response_dict = json.loads(response.text)
    except JSONDecodeError as e:
        raise AuthenticationError(
            f'{type(e).__name__}: Response returned by authentication server is invalid: {e}',
        ) from e

    headers_to_add: Dict = {}

    if headers is not None:
        for header_name, header_arg in headers.items():
            while '{{' in header_arg and '}}' in header_arg:
                # regex to find the name of the token inside {{token_name}}
                token_name = cast(Match, re.search('{{(.*)}}', header_arg)).group(1)

                # retrived token from the response
                res_token = _find_token(token_name.split('.'), response_dict)

                try:
                    if res_token is None:
                        raise AuthenticationError("The Authentication token wasn't fetched properly.")

                except AssertionError as e:
                    raise AuthenticationError(
                        f"{type(e).__name__}: The Authentication token wasn't fetched properly.",
                    ) from e

                header_arg = header_arg.replace('{{' + token_name + '}}', res_token)  # noqa: PLW2901

            headers_to_add[header_name] = header_arg

    # Here we are going to retrieve the refresh token from the response
    if refresh_token_name is not None:
        refresh_token: str = _find_token(refresh_token_name.split('.'), response_dict)
        return AuthResponse(tech=tech, headers=headers_to_add), refresh_token

    return AuthResponse(tech=tech, headers=headers_to_add), None


def hash_calculator(
    hash_type: AuthHashAlgorithmDigest,
    input_data: Union[str, bytes],
) -> str:
    """This function determines the appropriate hashing function and returns the hashing of the input."""

    if hash_type in (AuthHashAlgorithmDigest.MD5, AuthHashAlgorithmDigest.MD5_SESS):
        if isinstance(input_data, str):
            input_data = input_data.encode('utf-8')
        return hashlib.md5(input_data).hexdigest()  # noqa: S324

    if hash_type in (AuthHashAlgorithmDigest.SHA_256, AuthHashAlgorithmDigest.SHA_256_SESS):
        if isinstance(input_data, str):
            input_data = input_data.encode('utf-8')
        return hashlib.sha256(input_data).hexdigest()

    if hash_type in (AuthHashAlgorithmDigest.SHA_512_256, AuthHashAlgorithmDigest.SHA_512_256_SESS):
        if isinstance(input_data, str):
            input_data = input_data.encode('utf-8')
        return hashlib.sha512(input_data).hexdigest()

    return ''


def token_endpoint_auth_method(auth_location: AuthOAuthlocation) -> str:
    """This function takes the authorization location that is provided in the configuration
    and determines which token endpoint authentication method should be used by the session."""

    if auth_location == AuthOAuthlocation.BODY:
        return 'client_secret_post'
    if auth_location == AuthOAuthlocation.BASIC:
        return 'client_secret_basic'

    return ''  # type: ignore[unreachable]


def get_secret_hash(
    username: str,
    client_id: str,
    client_secret: str,
) -> str:
    """This function calculates the secret hash used in the AWS cognito
    authentication in case the client secret is provided."""

    message = bytearray(username + client_id, 'utf-8')
    hmac_obj = hmac.new(bytearray(client_secret, 'utf-8'), message, hashlib.sha256)
    return base64.standard_b64encode(hmac_obj.digest()).decode('utf-8')


def jwt_token_analyzer(token: Token) -> JWTToken:
    """This function transforms a JWT token into a defined datatype."""

    # First verify the JWT signature
    try:
        _ = jwt.decode(token, options={'verify_signature': False, 'verify_exp': False})
    except Exception as e:
        raise AuthenticationError('The token provided is not a JWT token') from e

    # First of all we need to decrypt the token
    separated_token = token.split('.')
    token_header: str = separated_token[0]
    token_payload: str = separated_token[1]

    header: Dict = json.loads(base64.urlsafe_b64decode(token_header + '=' * (-len(token_header) % 4)))
    payload: Dict = json.loads(base64.urlsafe_b64decode(token_payload + '=' * (-len(token_payload) % 4)))

    return JWTToken(
        {
            'sig': header['alg'],
            'iss': payload.pop('iss', None),
            'sub': payload.pop('sub', None),
            'aud': payload.pop('aud', None),
            'exp': payload.pop('exp', None),
            'nbf': payload.pop('nbf', None),
            'iat': payload.pop('iat', None),
            'jti': payload.pop('jti', None),
            'other': payload,
        },
    )


# def jwt_token_module(token: Token) -> None:
#     """This function takes in a JWT token as an input and analyzes the token
#     and finally returns some alerts regarding the JWT token."""

#     # First verify the JWT signature
#     try:
#         _ = jwt.decode(token, options={'verify_signature': False, 'verify_exp': False})
#     except Exception:
#         raise AuthenticationError('The token provided is not a JWT token')

#     # First divide the token into the header, payload, and signature
#     seperated_token = token.split('.')
#     token_header: str = seperated_token[0]
#     token_payload: str = seperated_token[1]
#     token_signature: str = seperated_token[2]

#     def _decode(string: Token) -> Dict:
#         return json.loads(base64.urlsafe_b64decode(string + '=' * (-len(string) % 4)))

#     def _encode(string: Dict) -> Token:
#         return base64.urlsafe_b64encode(json.dumps(string, separators=(',', ':')).encode()).decode('UTF-8').strip('=')

#     def _check_none_alg(token_header: str, token_payload: str) -> List[Token]:
#         """This function creates tokens with None signature."""

#         algorithms: List[str] = ['none', 'None', 'NONE', 'nOnE']
#         token_header_decoded: Dict = _decode(token_header)
#         result: List[str] = []

#         for algorithm in algorithms:
#             try:
#                 token_header_decoded['alg'] = algorithm
#             except KeyError:
#                 raise AuthenticationError('The header of the JWT token does not contain alg section')

#             result.append(_encode(token_header_decoded) + '.' + token_payload + '.')

#         return result

#     def _check_null_signature(token_header: str, token_payload: str) -> Token:
#         """This function creates a token with just null signature.

#         No changing of signing algorithm
#         """

#         return token_header + '.' + token_payload + '.'

#     def _check_hs_signature(token_header: str, token_payload: str) -> List[Token]:
#         """This function checks if it is possible to use a token with simply an hash signature."""

#         result: List[str] = []

#         # For sha512
#         new_header = _decode(deepcopy(token_header))
#         new_header['alg'] = 'HS512'
#         _new_header = _encode(new_header)
#         content = _new_header + '.' + token_payload
#         signature_hash_512 = base64.urlsafe_b64encode(hmac.new(''.encode(), content.encode(), hashlib.sha512,
#           ).digest()).decode('UTF-8').strip()
#         result.append(content + '.' + signature_hash_512)

#         # For sha256
#         new_header = _decode(deepcopy(token_header))
#         new_header['alg'] = 'HS256'
#         _new_header = _encode(new_header)
#         content = _new_header + '.' + token_payload
#         signature_hash_256 = base64.urlsafe_b64encode(hmac.new(''.encode(), content.encode(), hashlib.sha256,
#           ).digest()).decode('UTF-8').strip()
#         result.append(content + '.' + signature_hash_256)

#         # For sha384
#         new_header = _decode(deepcopy(token_header))
#         new_header['alg'] = 'HS384'
#         _new_header = _encode(new_header)
#         content = _new_header + '.' + token_payload
#         signature_hash_384 = base64.urlsafe_b64encode(hmac.new(''.encode(), content.encode(), hashlib.sha384,
#           ).digest()).decode('UTF-8').strip()
#         result.append(content + '.' + signature_hash_384)

#         return result

#     def _check_rsa_embed(token_header: str, token_payload: str) -> Token:
#         """Check in case the signature that RSA based."""

#         def _get_rsa_key_pair() -> Tuple[Any, Any]:
#             """Generate RSA keys."""

#             # generate private/public key pair
#             key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)

#             # get public key in OpenSSH format
#             public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH,
#               serialization.PublicFormat.OpenSSH)

#             # get private key in PEM container format
#             pem = key.private_bytes(
#                 encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL,
#                   encryption_algorithm=serialization.NoEncryption()
#             )

#             # decode to printable strings
#             private_key_str = pem.decode('utf-8')
#             public_key_str = public_key.decode('utf-8')

#             return private_key_str, public_key_str

#         priv_key, pub_key = _get_rsa_key_pair()
