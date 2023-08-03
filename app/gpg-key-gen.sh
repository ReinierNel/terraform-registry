#!/bin/bash

gpg --batch --gen-key gpg-settings
gpg --fingerprint | sed -n '4p' | sed 's/ //g' > gpg-fingerprint
echo '{}' > temp.json
jq --arg fingerprint "$(cat gpg-fingerprint)" '."fingerprint"=$fingerprint' <<<'{}' > temp.json
gpg --export --armor > gpg-ascii-armor
jq --arg armor "$(cat gpg-ascii-armor)" '."ascii-armor"=$armor' temp.json > gpg-registry-data.json
rm -rf temp.json
rm -rf gpg-ascii-armor
rm -rf gpg-fingerprint