from sqlalchemy.orm import Session
from . import models, schemas

def get_version_namespace_provider(db: Session, namespace: str, provider: str):

    fetch_version_data = db.query(models.Versions).filter(models.Versions.namespace == namespace).where(models.Versions.provider == provider).all()
    
    output = {
        "versions": []
    }
    
    for version in fetch_version_data:
        platforms = []
        fetch_provider_files = db.query(models.Provider_Package).filter(models.Provider_Package.version_id == version.id).all()
    
        for provider_files in fetch_provider_files:
            platforms.append({
                "os": provider_files.os,
                "arch": provider_files.arch
            })
    
        output["versions"].append(
            {
                "version": version.version,
                "protocols": version.protocols.split(","),
                "platforms": platforms
            }
        )
    
    return output

def get_provider_os_arch_version(db: Session, namespace: str, provider: str, version: str, operating_system: str, architecture: str):
    fetch_version_data = db.query(models.Versions) \
    .filter(models.Versions.namespace == namespace) \
    .where(models.Versions.provider == provider) \
    .where(models.Versions.version == version) \
    .one_or_none()

    fetch_provider_data = db.query(models.Provider_Package) \
    .filter(models.Provider_Package.version_id == fetch_version_data.id) \
    .where(models.Provider_Package.os == operating_system) \
    .where(models.Provider_Package.arch == architecture) \
    .one_or_none()

    fetch_signing_keys = db.query(models.Signing_Keys) \
    .where(models.Signing_Keys.id == fetch_provider_data.signing_keys_id) \
    .one_or_none()

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
                    "ascii_armor": fetch_signing_keys.ascii_armor
                }
            ]
        }
    }

    return output


# crud componetns
# version
def get_all_versions(db: Session):
    fech = db.query(models.Versions).all()
    output = []
    for data in fech:
        output.append(schemas.Version(
            version = data.version,
            namespace = data.namespace,
            id = data.id,
            protocols = data.protocols,
            provider = data.provider
    ))
    return output

def get_version_by_id(db: Session, id: int):
    fetch = db.query(models.Versions).where(models.Versions.id == id).one_or_none()
    output = schemas.Version(
        version = fetch.version,
        namespace = fetch.namespace,
        id = fetch.id,
        protocols = fetch.protocols,
        provider = fetch.provider
    )
    return output

def add_version(db: Session, version: schemas.Version):
    db_version = models.Versions(
        namespace = version.namespace,
        provider = version.provider,
        version = version.version,
        protocols = version.protocols
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version

def update_version(db: Session, version: schemas.Version):
    db_version = models.Versions(
        namespace = version.namespace,
        provider = version.provider,
        version = version.version,
        protocols = version.protocols,
        id = version.id
    )

    fetch = db.query(models.Versions).where(models.Versions.id == version.id).one_or_none()
    fetch.namespace = db_version.namespace
    fetch.provider = db_version.provider
    fetch.version = db_version.version
    fetch.protocols = db_version.protocols

    db.commit()
    db.refresh(fetch)
    return fetch

def delete_version_by_id(db: Session, id: int):
    db.query(models.Versions).filter(models.Versions.id == id).delete()
    try:
        db.commit()
    except:
        return False
    return True


