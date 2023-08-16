from pydantic import BaseModel, validator, UUID4

# Modules


# Provider
class Provider_Versions(BaseModel):
    versions: list = [
        {
            "version": "0.1.0",
            "protocols": ["4.0", "5.1"],
            "platforms": [
                {"os": "darwin", "arch": "amd64"},
                {"os": "darwin", "arch": "arm64"},
                {"os": "linux", "arch": "amd64"},
                {"os": "linux", "arch": "arm64"},
                {"os": "windows", "arch": "amd64"},
                {"os": "windows", "arch": "arm64"},
            ],
        }
    ]


class Provider_Packages(BaseModel):
    protocols: list[str]
    os: str
    arch: str
    filename: str
    download_url: str
    shasums_url: str
    shasums_signature_url: str
    shasum: str
    signing_keys: dict = {"gpg_public_keys": [{"key_id": "", "ascii_armor": ""}]}


class Provider_Version(BaseModel):
    version: str
    namespace: str
    id: UUID4 = None
    protocols: str
    provider: str


class Provider_Package(BaseModel):
    id: UUID4 = None
    filename: str
    download_url: str
    shasums_url: str
    shasums_signature_url: str
    shasum: str
    signing_keys_id: UUID4
    os: str
    arch: str
    version_id: UUID4


class Provider_GPG_Public_Keys(BaseModel):
    id: UUID4 = None
    key_id: str
    ascii_armor: str
