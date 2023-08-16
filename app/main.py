from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from pydantic import UUID4
from json import load
from os import getenv

# Metadata
models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Service Discovery",
        "externalDocs": {
            "description": "Terraform Internals Documentation",
            "url": "https://developer.hashicorp.com/terraform/internals/remote-service-discovery",
        },
    },
    {
        "name": "Module Registry Protocol",
        "externalDocs": {
            "description": "Terraform Internals Documentation",
            "url": "https://developer.hashicorp.com/terraform/internals/module-registry-protocol",
        },
    },
    {
        "name": "Module Versions CRUD",
        "description": "Endpoints to manage module versions (Create, Read, Update, Delete)",
    },
    {
        "name": "Module Download URL CRUD",
        "description": "Endpoints to manage module download links (Create, Read, Update, Delete)",
    },
    {
        "name": "Provider GPG Public Keys CRUD",
        "description": "Endpoints to manage provider singing pgp public keys (Create, Read, Update, Delete)",
    },
    {
        "name": "Provider Registry Protocol",
        "externalDocs": {
            "description": "Terraform Internals Documentation",
            "url": "https://developer.hashicorp.com/terraform/internals/provider-registry-protocol",
        },
    },
    {
        "name": "Provider Versions CRUD",
        "description": "Endpoints to manage provider versions (Create, Read, Update, Delete)",
    },
    {
        "name": "Provider Package CRUD",
        "description": "Endpoints to manage provider packages (Create, Read, Update, Delete)",
    },
    {
        "name": "Provider GPG Public Keys CRUD",
        "description": "Endpoints to manage provider singing pgp public keys (Create, Read, Update, Delete)",
    },
]

version_file = open("/code/app/version.json")
version_data = load(version_file)
version_file.close()

app = FastAPI(
    title="Terraform Private Registry",
    version=version_data["version"],
    contact={
        "name": "Reinier Nel",
        "url": "https://reinier.co.za",
        "email": "hi@reinier.co.za",
    },
    license_info={
        "name": "MIT",
        "url": "https://raw.githubusercontent.com/ReinierNel/terraform-registry/main/LICENSE",
    },
    openapi_tags=tags_metadata,
)


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
Discovery Endpoints
"""


# set uri base path if env var
if getenv("TF_REG_BASE_PATH") is None:
    base_path = ""
else:
    base_path = "/" + getenv("TF_REG_BASE_PATH")


# https://developer.hashicorp.com/terraform/internals/provider-registry-protocol
@app.get("/.well-known/terraform.json", tags=["Service Discovery"])
def service_discovery():
    return {
        "providers.v1": base_path + "/providers/v1/",
        "modules.v1": base_path + "/modules/v1/",
    }


"""
Module Endpoints
"""


# List Available Versions
@app.get(
    base_path + "/modules/v1/{namespace}/{name}/{system}/versions",
    # response_model=schemas.Versions,
    tags=["Module Registry Protocol"],
)
def available_module_versions(namespace: str, name: str, system: str):
    return {
        "modules": [
            {
                "versions": [
                    {"version": "1.0.0"},
                    {"version": "1.1.0"},
                    {"version": "2.0.0"},
                ]
            }
        ]
    }


# Download Source Code
@app.get(
    base_path + "/modules/v1/{namespace}/{name}/{system}/{version}/download",
    status_code=204,
    tags=["Module Registry Protocol"],
)
def source_download_location(
    namespace: str, module: str, system: str, version: str, response: Response
):
    response.headers["X-Terraform-Get"] = "https://some-location-to-download-from"
    return None


# Version CRUD

# Download Source Crud

"""
Provider Endpoints
"""


# List Available Versions
@app.get(
    base_path + "/providers/v1/{namespace}/{type}/versions",
    response_model=schemas.Provider_Versions,
    tags=["Provider Registry Protocol"],
)
def available_versions(namespace: str, type: str, db: Session = Depends(get_db)):
    fetch = crud.get_version_namespace_provider(
        db=db, namespace=namespace, provider=type
    )
    if fetch is None:
        raise HTTPException(status_code=404, detail="404 Not Found")
    return fetch


# Find a Provider Package
@app.get(
    base_path
    + "/providers/v1/{namespace}/{type}/{version}/download/{operating_system}/{architecture}",
    response_model=schemas.Provider_Packages,
    tags=["Provider Registry Protocol"],
)
def provider_package(
    namespace: str,
    type: str,
    version: str,
    operating_system: str,
    architecture: str,
    db: Session = Depends(get_db),
):
    fetch = crud.get_provider_os_arch_version(
        namespace=namespace,
        provider=type,
        version=version,
        operating_system=operating_system,
        architecture=architecture,
        db=db,
    )
    if fetch is None:
        raise HTTPException(status_code=404, detail="404 Not Found")
    return fetch


# Versions CRUD
@app.get(
    base_path + "/providers/v1/versions/getall",
    response_model=list[schemas.Provider_Version],
    tags=["Provider Versions CRUD"],
)
def get_all_versions(db: Session = Depends(get_db)):
    return crud.get_all_versions(db=db)


@app.get(
    base_path + "/providers/v1/versions/get",
    response_model=schemas.Provider_Version,
    tags=["Provider Versions CRUD"],
)
def get_versions_by_id(id: UUID4, db: Session = Depends(get_db)):
    return crud.get_version_by_id(db=db, id=id)


@app.post(
    base_path + "/providers/v1/versions/add",
    response_model=schemas.Provider_Version,
    tags=["Provider Versions CRUD"],
    status_code=201,
)
def add_versions(version: schemas.Provider_Version, db: Session = Depends(get_db)):
    data = crud.add_version(db=db, version=version)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


@app.put(
    base_path + "/providers/v1/versions/update",
    response_model=schemas.Provider_Version,
    tags=["Provider Versions CRUD"],
)
def update_versions_by_id(
    version: schemas.Provider_Version, db: Session = Depends(get_db)
):
    data = crud.update_version(db=db, version=version)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


@app.delete(
    base_path + "/providers/v1/versions/delete", tags=["Provider Versions CRUD"]
)
def delete_versions_by_id(id: UUID4, db: Session = Depends(get_db)):
    if crud.delete_version_by_id(db=db, id=id):
        return {"details": "200 OK"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


# Package CRUD
@app.get(
    base_path + "/providers/v1/package/getall",
    response_model=list[schemas.Provider_Package],
    tags=["Provider Package CRUD"],
)
def get_all_package(db: Session = Depends(get_db)):
    return crud.get_all_package(db=db)


@app.get(
    base_path + "/providers/v1/package/get",
    response_model=schemas.Provider_Package,
    tags=["Provider Package CRUD"],
)
def get_package_by_id(id: UUID4, db: Session = Depends(get_db)):
    return crud.get_package_by_id(db=db, id=id)


@app.post(
    base_path + "/providers/v1/package/add",
    response_model=schemas.Provider_Package,
    tags=["Provider Package CRUD"],
    status_code=201,
)
def add_package(version: schemas.Provider_Package, db: Session = Depends(get_db)):
    data = crud.add_package(db=db, version=version)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


@app.put(
    base_path + "/providers/v1/package/update",
    response_model=schemas.Provider_Package,
    tags=["Provider Package CRUD"],
)
def update_package_by_id(
    version: schemas.Provider_Package, db: Session = Depends(get_db)
):
    data = crud.update_package_by_id(db=db, version=version)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


@app.delete(base_path + "/providers/v1/package/delete", tags=["Provider Package CRUD"])
def delete_package_by_id(id: UUID4, db: Session = Depends(get_db)):
    if crud.delete_package_by_id(db=db, id=id):
        return {"details": "200 OK"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


# GPG_Public_Keys CRUD
@app.get(
    base_path + "/providers/v1/gpg-public-key/getall",
    response_model=list[schemas.Provider_GPG_Public_Keys],
    tags=["Provider GPG Public Keys CRUD"],
)
def get_all_gpg_public_keys(db: Session = Depends(get_db)):
    return crud.get_all_gpg_public_keys(db=db)


@app.get(
    base_path + "/providers/v1/gpg-public-key/get",
    response_model=schemas.Provider_GPG_Public_Keys,
    tags=["Provider GPG Public Keys CRUD"],
)
def get_provider_gpg_public_key_by_id(id: UUID4, db: Session = Depends(get_db)):
    return crud.get_provider_gpg_public_key_by_id(db=db, id=id)


@app.post(
    base_path + "/providers/v1/gpg-public-key/add",
    response_model=schemas.Provider_GPG_Public_Keys,
    tags=["Provider GPG Public Keys CRUD"],
    status_code=201,
)
def add_gpg_public_key(
    gpg_public_key: schemas.Provider_GPG_Public_Keys, db: Session = Depends(get_db)
):
    data = crud.add_gpg_public_key(db=db, gpg_public_key=gpg_public_key)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


@app.put(
    base_path + "/providers/v1/gpg-public-key/update",
    response_model=schemas.Provider_GPG_Public_Keys,
    tags=["Provider GPG Public Keys CRUD"],
)
def update_gpg_public_key_by_id(
    gpg_public_key: schemas.Provider_GPG_Public_Keys, db: Session = Depends(get_db)
):
    data = crud.update_gpg_public_key_by_id(db=db, gpg_public_key=gpg_public_key)
    if data is not None:
        return data
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


@app.delete(
    base_path + "/providers/v1/gpg-public-key/delete",
    tags=["Provider GPG Public Keys CRUD"],
)
def delete_gpg_public_key_by_id(id: UUID4, db: Session = Depends(get_db)):
    if crud.delete_gpg_public_key_by_id(db=db, id=id):
        return {"details": "200 OK"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")
