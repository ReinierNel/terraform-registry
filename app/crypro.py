import os
import json
"""
shasum -a 256 terraform-provider-keystore_0.1.0_darwin-arm64.zip > terraform-provider-keystore_0.1.0_darwin_arm64_SHA256SUMS

gpg --detach-sign terraform-provider-keystore_0.1.0_darwin_arm64_SHA256SUMS
gpg --armor --export-secret-keys 3CBBBF4265AFBD7ED7886C77BB483F02D300C1C7 > private_key.gpg
jq --arg armor "$(cat public.key)" '.data.attributes."ascii-armor"=$armor' ../../terraform-private-provider-registry/app/providers/hashicorp/keystore.json > gpg-payload.json
gpg --fingerprint
"""
def generate_gpg_keys():
    os.system("bash gpg-key-gen.sh")
    json_file = open("gpg-registry-data.json")
    json.load(json_file)
    json_file.close()

generate_gpg_keys()

