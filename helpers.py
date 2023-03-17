from urllib.parse import urlparse

from bech32 import bech32_decode, convertbits
from starlette.responses import JSONResponse


def normalize_public_key(pubkey: str) -> str:
    if pubkey.startswith("npub1"):
        _, decoded_data = bech32_decode(pubkey)
        if not decoded_data:
            raise ValueError("Public Key is not valid npub")

        decoded_data_bits = convertbits(decoded_data, 5, 8, False)
        if not decoded_data_bits:
            raise ValueError("Public Key is not valid npub")
        return bytes(decoded_data_bits).hex()

    # check if valid hex
    if len(pubkey) != 64:
        raise ValueError("Public Key is not valid hex")
    int(pubkey, 16)
    return pubkey


def extract_domain(url: str) -> str:
    return urlparse(url).netloc


def relay_info_response(relay_public_data: dict) -> JSONResponse:
    return JSONResponse(
        content=relay_public_data,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET",
        },
    )
