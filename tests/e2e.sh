#!/bin/bash

function test() {

    METHOD="$1"
    ENDPOINT="$2"
    DATA="$3"

    COMPONENT="$5"
    COMPARE="$6"

    if [[ "$DATA" == "" ]]; then
        RESPONCE=$(curl -k -s -X "$METHOD" \
        "https://localhost/$ENDPOINT" \
        -H 'accept: application/json')
    else
        RESPONCE=$(curl -k -s -X "$METHOD" \
        "https://localhost/$ENDPOINT" \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d "$DATA")
    fi
    
    case "$4" in
        EQ)
            if [[ $(jq -r "$COMPONENT" <<<"$RESPONCE") == "$COMPARE" ]]; then
                STATUS="[ pass ]"
            else
                STATUS="[ fail ]"
            fi
        ;;
        REGEX)
            if [[ $(jq -r "$COMPONENT" <<<"$RESPONCE") =~ $COMPARE ]]; then
                STATUS="[ pass ]"
            else
                STATUS="[ fail ]"
            fi
        ;;
        LE)
            if [[ $(jq -r "$COMPONENT" <<<"$RESPONCE") -le $COMPARE ]]; then
                STATUS="[ pass ]"
            else
                STATUS="[ fail ]"
            fi
        ;;
        GE)
            if [[ $(jq -r "$COMPONENT" <<<"$RESPONCE") -ge $COMPARE ]]; then
                STATUS="[ pass ]"
            else
                STATUS="[ fail ]"
            fi
        ;;
        LT)
            if [[ $(jq -r "$COMPONENT" <<<"$RESPONCE") -lt $COMPARE ]]; then
                STATUS="[ pass ]"
            else
                STATUS="[ fail ]"
            fi
        ;;
        GT)
            if [[ $(jq -r "$COMPONENT" <<<"$RESPONCE") -gt $COMPARE ]]; then
                STATUS="[ pass ]"
            else
                STATUS="[ fail ]"
            fi
        ;;
    esac
    echo "$STATUS $METHOD $ENDPOINT"
    if [[ "$7" != "" ]]; then
        echo "$RESPONCE" > "$7"
    fi
}

# Provider Version

test 'POST' \
'providers/v1/versions/add' \
"$(jq -r .version data.json)" \
'REGEX' \
'.id' \
'^\{?[A-F0-9a-f]{8}-[A-F0-9a-f]{4}-[A-F0-9a-f]{4}-[A-F0-9a-f]{4}-[A-F0-9a-f]{12}\}?$' \
'provider_version_put.json'

test 'GET' \
'providers/v1/versions/getall' \
'' \
'GE' \
'length' \
1

PROVIDER_VERSION_ID=$(jq -r .id provider_version_put.json)

test 'GET' \
"providers/v1/versions/get?id=$PROVIDER_VERSION_ID" \
'' \
'EQ' \
'.id' \
"$PROVIDER_VERSION_ID"

test 'PUT' \
"providers/v1/versions/update" \
"{\"version\": \"0.1.0\",\"namespace\": \"reiniernel89\",\"id\": \"$PROVIDER_VERSION_ID\",\"protocols\": \"4.0,5.1\",\"provider\": \"privatetfreg\"}" \
'EQ' \
'.provider' \
"privatetfreg"


# GPG Keys
test 'POST' \
'providers/v1/gpg-public-key/add' \
"$(jq -r .signing_keys data.json)" \
'REGEX' \
'.id' \
'^\{?[A-F0-9a-f]{8}-[A-F0-9a-f]{4}-[A-F0-9a-f]{4}-[A-F0-9a-f]{4}-[A-F0-9a-f]{12}\}?$' \
'provider_keys_put.json'

test 'GET' \
'providers/v1/gpg-public-key/getall' \
'' \
'GE' \
'length' \
1

PROVIDER_KEY_ID=$(jq -r .id provider_keys_put.json)

test 'GET' \
"providers/v1/gpg-public-key/get?id=$PROVIDER_KEY_ID" \
'' \
'EQ' \
'.id' \
"$PROVIDER_KEY_ID"

test 'PUT' \
"providers/v1/gpg-public-key/update" \
"{\"id\": \"$PROVIDER_KEY_ID\",\"key_id\": \"51852D87348FFC4C\",\"ascii_armor\": \"-----BEGIN PGP PUBLIC KEY BLOCK-----\nVersion: GnuPG v1\n\nmQENBFMORM0BCADBRyKO1MhCirazOSVwcfTr1xUxjPvfxD3hjUwHtjsOy/bT6p9f\nW2mRPfwnq2JB5As+paL3UGDsSRDnK9KAxQb0NNF4+eVhr/EJ18s3wwXXDMjpIifq\nfIm2WyH3G+aRLTLPIpscUNKDyxFOUbsmgXAmJ46Re1fn8uKxKRHbfa39aeuEYWFA\n3drdL1WoUngvED7f+RnKBK2G6ZEpO+LDovQk19xGjiMTtPJrjMjZJ3QXqPvx5wca\nKSZLr4lMTuoTI/ZXyZy5bD4tShiZz6KcyX27cD70q2iRcEZ0poLKHyEIDAi3TM5k\nSwbbWBFd5RNPOR0qzrb/0p9ksKK48IIfH2FvABEBAAG0K0hhc2hpQ29ycCBTZWN1\ncml0eSA8c2VjdXJpdHlAaGFzaGljb3JwLmNvbT6JATgEEwECACIFAlMORM0CGwMG\nCwkIBwMCBhUIAgkKCwQWAgMBAh4BAheAAAoJEFGFLYc0j/xMyWIIAIPhcVqiQ59n\nJc07gjUX0SWBJAxEG1lKxfzS4Xp+57h2xxTpdotGQ1fZwsihaIqow337YHQI3q0i\nSqV534Ms+j/tU7X8sq11xFJIeEVG8PASRCwmryUwghFKPlHETQ8jJ+Y8+1asRydi\npsP3B/5Mjhqv/uOK+Vy3zAyIpyDOMtIpOVfjSpCplVRdtSTFWBu9Em7j5I2HMn1w\nsJZnJgXKpybpibGiiTtmnFLOwibmprSu04rsnP4ncdC2XRD4wIjoyA+4PKgX3sCO\nklEzKryWYBmLkJOMDdo52LttP3279s7XrkLEE7ia0fXa2c12EQ0f0DQ1tGUvyVEW\nWmJVccm5bq25AQ0EUw5EzQEIANaPUY04/g7AmYkOMjaCZ6iTp9hB5Rsj/4ee/ln9\nwArzRO9+3eejLWh53FoN1rO+su7tiXJA5YAzVy6tuolrqjM8DBztPxdLBbEi4V+j\n2tK0dATdBQBHEh3OJApO2UBtcjaZBT31zrG9K55D+CrcgIVEHAKY8Cb4kLBkb5wM\nskn+DrASKU0BNIV1qRsxfiUdQHZfSqtp004nrql1lbFMLFEuiY8FZrkkQ9qduixo\nmTT6f34/oiY+Jam3zCK7RDN/OjuWheIPGj/Qbx9JuNiwgX6yRj7OE1tjUx6d8g9y\n0H1fmLJbb3WZZbuuGFnK6qrE3bGeY8+AWaJAZ37wpWh1p0cAEQEAAYkBHwQYAQIA\nCQUCUw5EzQIbDAAKCRBRhS2HNI/8TJntCAClU7TOO/X053eKF1jqNW4A1qpxctVc\nz8eTcY8Om5O4f6a/rfxfNFKn9Qyja/OG1xWNobETy7MiMXYjaa8uUx5iFy6kMVaP\n0BXJ59NLZjMARGw6lVTYDTIvzqqqwLxgliSDfSnqUhubGwvykANPO+93BBx89MRG\nunNoYGXtPlhNFrAsB1VR8+EyKLv2HQtGCPSFBhrjuzH3gxGibNDDdFQLxxuJWepJ\nEK1UbTS4ms0NgZ2Uknqn1WRU1Ki7rE4sTy68iZtWpKQXZEJa0IGnuI2sSINGcXCJ\noEIgXTMyCILo34Fa/C6VCm2WBgz9zZO8/rHIiQm1J5zqz0DrDwKBUM9C\n=LYpS\n-----END PGP PUBLIC KEY BLOCK-----\"}" \
'EQ' \
'.key_id' \
"51852D87348FFC4C"


# provider Packages
test 'POST' \
'providers/v1/package/add' \
"$(jq -r .package data.json | jq ".version_id = \"$PROVIDER_KEY_ID\"" | jq ".signing_keys_id = \"$PROVIDER_VERSION_ID\"")" \
'REGEX' \
'.id' \
'^\{?[A-F0-9a-f]{8}-[A-F0-9a-f]{4}-[A-F0-9a-f]{4}-[A-F0-9a-f]{4}-[A-F0-9a-f]{12}\}?$' \
'provider_package_put.json'

test 'GET' \
'providers/v1/package/getall' \
'' \
'GE' \
'length' \
1

PROVIDER_PACKAGE_ID=$(jq -r .id provider_package_put.json)

test 'GET' \
"providers/v1/gpg-public-key/get?id=$PROVIDER_PACKAGE_ID" \
'' \
'EQ' \
'.id' \
"$PROVIDER_PACKAGE_ID"

test 'PUT' \
"providers/v1/gpg-public-key/update" \
"$(jq -r .package data.json | jq ".version_id = \"$PROVIDER_KEY_ID\"" | jq ".signing_keys_id = \"$PROVIDER_VERSION_ID\"")" \
'EQ' \
'.filename' \
"terraform-provider-random_2.0.0_linux_amd64.zip"



# Delete Tests
# test 'DELETE' \
# "providers/v1/versions/delete?id=$PROVIDER_VERSION_ID" \
# "" \
# 'EQ' \
# '.details' \
# "200 OK"

# test 'DELETE' \
# "providers/v1/gpg-public-key/delete?id=$PROVIDER_KEY_ID" \
# "" \
# 'EQ' \
# '.details' \
# "200 OK"

# test 'DELETE' \
# "providers/v1/gpg-public-key/delete?id=$PROVIDER_PACKAGE_ID" \
# "" \
# 'EQ' \
# '.details' \
# "200 OK"