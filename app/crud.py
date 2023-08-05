from sqlalchemy.orm import Session
from . import models, schemas
from pydantic import UUID4


def get_version_namespace_provider(db: Session, namespace: str, provider: str):
    fetch_version_data = (
        db.query(models.Versions)
        .filter(models.Versions.namespace == namespace)
        .where(models.Versions.provider == provider)
        .all()
    )

    output = {"versions": []}

    for version in fetch_version_data:
        platforms = []
        fetch_provider_files = (
            db.query(models.Provider_Package)
            .filter(models.Provider_Package.version_id == version.id)
            .all()
        )

        for provider_files in fetch_provider_files:
            platforms.append({"os": provider_files.os, "arch": provider_files.arch})

        output["versions"].append(
            {
                "version": version.version,
                "protocols": version.protocols.split(","),
                "platforms": platforms,
            }
        )

    return output


def get_provider_os_arch_version(
    db: Session,
    namespace: str,
    provider: str,
    version: str,
    operating_system: str,
    architecture: str,
):
    fetch_version_data = (
        db.query(models.Versions)
        .filter(models.Versions.namespace == namespace)
        .where(models.Versions.provider == provider)
        .where(models.Versions.version == version)
        .one_or_none()
    )

    fetch_provider_data = (
        db.query(models.Provider_Package)
        .filter(models.Provider_Package.version_id == fetch_version_data.id)
        .where(models.Provider_Package.os == operating_system)
        .where(models.Provider_Package.arch == architecture)
        .one_or_none()
    )

    fetch_signing_keys = (
        db.query(models.Signing_Keys)
        .where(models.Signing_Keys.id == fetch_provider_data.signing_keys_id)
        .one_or_none()
    )

    output = {
        "protocols": fetch_version_data.protocols.split(","),
        "os": fetch_provider_data.os,
        "arch": fetch_provider_data.arch,
        "filename": fetch_provider_data.filename,
        "download_url": fetch_provider_data.download_url,
        "shasums_url": fetch_provider_data.shasums_url,
        "shasums_signature_url": fetch_provider_data.shasums_signature_url,
        "shasum": fetch_provider_data.shasum,
        "signing_keys": {
            "gpg_public_keys": [
                {
                    "key_id": fetch_signing_keys.key_id,
                    "ascii_armor": fetch_signing_keys.ascii_armor,
                }
            ]
        },
    }

    return output


# crud components


# version
def get_all_versions(db: Session):
    fech = db.query(models.Versions).all()
    output = []
    for data in fech:
        output.append(
            schemas.Version(
                version=data.version,
                namespace=data.namespace,
                id=data.id,
                protocols=data.protocols,
                provider=data.provider,
            )
        )
    return output


def get_version_by_id(db: Session, id: UUID4):
    fetch = db.query(models.Versions).where(models.Versions.id == id).one_or_none()
    output = schemas.Version(
        version=fetch.version,
        namespace=fetch.namespace,
        id=fetch.id,
        protocols=fetch.protocols,
        provider=fetch.provider,
    )
    return output


def add_version(db: Session, version: schemas.Version):
    db_version = models.Versions(
        namespace=version.namespace,
        provider=version.provider,
        version=version.version,
        protocols=version.protocols,
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version


def update_version(db: Session, version: schemas.Version):
    db_version = models.Versions(
        namespace=version.namespace,
        provider=version.provider,
        version=version.version,
        protocols=version.protocols,
        id=version.id,
    )

    fetch = (
        db.query(models.Versions).where(models.Versions.id == version.id).one_or_none()
    )
    fetch.namespace = db_version.namespace
    fetch.provider = db_version.provider
    fetch.version = db_version.version
    fetch.protocols = db_version.protocols

    db.commit()
    db.refresh(fetch)
    return fetch


def delete_version_by_id(db: Session, id: UUID4):
    db.query(models.Versions).filter(models.Versions.id == id).delete()
    try:
        db.commit()
    except:
        return False
    return True


def get_signing_keys_by_public_id(db: Session, pub_id: str):
    fetch = (
        db.query(models.Signing_Keys)
        .where(models.Signing_Keys.key_id == pub_id)
        .one_or_none()
    )
    output = schemas.Signing_Keys(
        id=fetch.id, key_id=fetch.key_id, ascii_armor=fetch.ascii_armor
    )
    return output


# provider package
def get_all_package(db: Session):
    fetch = db.query(models.Package).all()
    output = []
    for data in fetch:
        output.append(
            schemas.Package(
                id=data.id,
                filename=data.filename,
                download_url=data.download_url,
                shasums_url=data.shasums_url,
                shasums_signature_url=data.shasums_signature_url,
                shasum=data.shasum,
                signing_keys_id=data.signing_keys_id,
                os=data.os,
                arch=data.arch,
                version_id=data.version_id,
            )
        )
    return output


def get_package_by_id(db: Session, id: UUID4):
    fetch = db.query(models.Package).where(models.Package.id == id).one_or_none()
    output = schemas.Package(
        id=fetch.id,
        filename=fetch.filename,
        download_url=fetch.download_url,
        shasums_url=fetch.shasums_url,
        shasums_signature_url=fetch.shasums_signature_url,
        shasum=fetch.shasum,
        signing_keys_id=fetch.signing_keys_id,
        os=fetch.os,
        arch=fetch.arch,
        version_id=fetch.version_id,
    )
    return output


def add_package(db: Session, version: schemas.Package):
    db_version = models.Package(
        id=version.id,
        filename=version.filename,
        download_url=version.download_url,
        shasums_url=version.shasums_url,
        shasums_signature_url=version.shasums_signature_url,
        shasum=version.shasum,
        signing_keys_id=version.signing_keys_id,
        os=version.os,
        arch=version.arch,
        version_id=version.version_id,
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version


def update_package_by_id(db: Session, version: schemas.Package):
    fetch = (
        db.query(models.Package).where(models.Package.id == version.id).one_or_none()
    )

    fetch.filename = (version.filename,)
    fetch.download_url = (version.download_url,)
    fetch.shasums_url = (version.shasums_url,)
    fetch.shasums_signature_url = (version.shasums_signature_url,)
    fetch.shasum = (version.shasum,)
    fetch.signing_keys_id = (version.signing_keys_id,)
    fetch.os = (version.os,)
    fetch.arch = (version.arch,)
    fetch.version_id = (version.version_id,)

    db.commit()
    db.refresh(fetch)
    return fetch


def delete_package_by_id(db: Session, id: UUID4):
    db.query(models.Package).filter(models.Package.id == id).delete()
    try:
        db.commit()
    except:
        return False
    return True


# gpg public keys
def get_all_gpg_public_keys(db: Session):
    fetch = db.query(models.GPG_Public_Keys).all()
    output = []
    for data in fetch:
        output.append(
            schemas.Package(
                id=data.id, key_id=data.key_id, ascii_armor=data.ascii_armor
            )
        )
    return output


def get_provider_gpg_public_key_by_id(db: Session, id: UUID4):
    fetch = (
        db.query(models.GPG_Public_Keys)
        .where(models.GPG_Public_Keys.id == id)
        .one_or_none()
    )
    output = schemas.GPG_Public_Keys(
        id=fetch.id, key_id=fetch.key_id, ascii_armor=fetch.ascii_armor
    )
    return output


def add_gpg_public_key(db: Session, gpg_public_key: schemas.GPG_Public_Keys):
    db_version = models.GPG_Public_Keys(
        id=gpg_public_key.id,
        key_id=gpg_public_key.key_id,
        ascii_armor=gpg_public_key.ascii_armor,
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version


def update_gpg_public_key_by_id(db: Session, gpg_public_key: schemas.GPG_Public_Keys):
    fetch = (
        db.query(models.GPG_Public_Keys)
        .where(models.GPG_Public_Keys.id == gpg_public_key.id)
        .one_or_none()
    )

    fetch.key_id = gpg_public_key.key_id
    fetch.ascii_armor = gpg_public_key.ascii_armor

    db.commit()
    db.refresh(fetch)
    return fetch


def delete_gpg_public_key_by_id(db: Session, id: UUID4):
    db.query(models.GPG_Public_Keys).filter(models.GPG_Public_Keys.id == id).delete()
    try:
        db.commit()
    except:
        return False
    return True
