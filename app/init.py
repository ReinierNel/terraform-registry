import os
import json
from . import crud

"""
shasum -a 256 terraform-provider-keystore_0.1.0_darwin-arm64.zip > terraform-provider-keystore_0.1.0_darwin_arm64_SHA256SUMS

gpg --detach-sign terraform-provider-keystore_0.1.0_darwin_arm64_SHA256SUMS
gpg --armor --export-secret-keys 3CBBBF4265AFBD7ED7886C77BB483F02D300C1C7 > private_key.gpg
jq --arg armor "$(cat public.key)" '.data.attributes."ascii-armor"=$armor' ../../terraform-private-provider-registry/app/providers/hashicorp/keystore.json > gpg-payload.json
gpg --fingerprint
"""
def generate_gpg_keys() -> dict:
    os.system(f"bash /code/app/gpg-key-gen.sh '/code/app'")
    json_file = open("/code/app/gpg-registry-data.json")
    data = json.load(json_file)
    json_file.close()
    return data
