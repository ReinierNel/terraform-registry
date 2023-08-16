#!/bin/bash

path="$1"

gpg --batch --gen-key "$path"/gpg-settings
gpg --fingerprint | sed -n '4p' | sed 's/ //g' > "$path"/gpg-fingerprint
echo '{}' > "$path"/temp.json
jq --arg fingerprint "$(cat gpg-fingerprint)" '."fingerprint"=$fingerprint' <<<'{}' > "$path"/temp.json
gpg --export --armor >  "$path"/gpg-ascii-armor
jq --arg armor "$(cat gpg-ascii-armor)" '."ascii-armor"=$armor' "$path"/temp.json > "$path"/gpg-registry-data.json
rm -rf "$path"/temp.json
rm -rf "$path"/gpg-ascii-armor
rm -rf "$path"/gpg-fingerprint