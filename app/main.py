from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, init
from .database import SessionLocal, engine
from pydantic import UUID4

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# https://developer.hashicorp.com/terraform/internals/provider-registry-protocol
@app.get("/.well-known/terraform.json", tags=["Provider Registry Protocol"])
def service_discovery():
    return {"providers.v1": "/terraform/providers/v1/"}


@app.get(
    "/v1/providers/{namespace}/{provider}/versions",
    response_model=schemas.Versions,
    tags=["Provider Registry Protocol"],
)
def available_versions(namespace: str, provider: str, db: Session = Depends(get_db)):
    fetch = crud.get_version_namespace_provider(
        db=db, namespace=namespace, provider=provider
    )
    if fetch is None:
        raise HTTPException(status_code=404, detail="404 Not Found")
    return fetch


@app.get(
    "/v1/providers/{namespace}/{provider}/{version}/download/{operating_system}/{architecture}",
    response_model=schemas.Provider_Package,
    tags=["Provider Registry Protocol"],
)
def provider_package(
    namespace: str,
    provider: str,
    version: str,
    operating_system: str,
    architecture: str,
    db: Session = Depends(get_db),
):
    fetch = crud.get_provider_os_arch_version(
        namespace=namespace,
        provider=provider,
        version=version,
        operating_system=operating_system,
        architecture=architecture,
        db=db,
    )
    if fetch is None:
        raise HTTPException(status_code=404, detail="404 Not Found")
    return fetch


# Management CURD
# Versions
@app.get("/v1/versions/getall", response_model=list[schemas.Version], tags=["Versions"])
def get_all_versions(db: Session = Depends(get_db)):
    return crud.get_all_versions(db=db)


@app.get("/v1/versions/get", response_model=schemas.Version, tags=["Versions"])
def get_versions_by_id(id: UUID4, db: Session = Depends(get_db)):
    return crud.get_version_by_id(db=db, id=id)


@app.post("/v1/versions/add", tags=["Versions"], status_code=201)
def add_versions(version: schemas.Version, db: Session = Depends(get_db)):
    if crud.add_version(db=db, version=version):
        return {"details": "201 Created"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


# response_model=schemas.Versions
@app.put("/v1/versions/update", tags=["Versions"])
def update_versions_by_id(version: schemas.Version, db: Session = Depends(get_db)):
    if crud.update_version(db=db, version=version):
        return {"details": "200 OK"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


@app.delete("/v1/versions/delete", tags=["Versions"])
def delete_versions_by_id(id: UUID4, db: Session = Depends(get_db)):
    if crud.delete_version_by_id(db=db, id=id):
        return {"details": "200 OK"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


# Provider_Package
@app.get(
    "/v1/package/getall",
    response_model=list[schemas.Package],
    tags=["Package"],
)
def get_all_package(db: Session = Depends(get_db)):
    return crud.get_all_provider_package(db=db)


@app.get("/v1/package/get", response_model=schemas.Package, tags=["Package"])
def get_package_by_id(id: UUID4, db: Session = Depends(get_db)):
    return crud.get_package_by_id(db=db, id=id)


@app.post("/v1/package/add", tags=["Package"], status_code=201)
def add_package(version: schemas.Package, db: Session = Depends(get_db)):
    if crud.add_package(db=db, version=version):
        return {"details": "201 Created"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


# response_model=schemas.Versions
@app.put("/v1/package/update", tags=["Package"])
def update_package_by_id(version: schemas.Package, db: Session = Depends(get_db)):
    if crud.update_package_by_id(db=db, version=version):
        return {"details": "200 OK"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


@app.delete("/v1/package/delete", tags=["Package"])
def delete_package_by_id(id: UUID4, db: Session = Depends(get_db)):
    if crud.delete_package_by_id(db=db, id=id):
        return {"details": "200 OK"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


# GPG_Public_Keys
@app.get(
    "/v1/gpg-public-key/getall",
    response_model=list[schemas.GPG_Public_Keys],
    tags=["GPG Public Keys"],
)
def get_all_gpg_public_keys(db: Session = Depends(get_db)):
    return crud.get_all_gpg_public_keys(db=db)


@app.get(
    "/v1/gpg-public-key/get",
    response_model=schemas.GPG_Public_Keys,
    tags=["GPG Public Keys"],
)
def get_provider_gpg_public_key_by_id(id: UUID4, db: Session = Depends(get_db)):
    return crud.get_provider_gpg_public_key_by_id(db=db, id=id)


@app.post("/v1/gpg-public-key/add", tags=["GPG Public Keys"], status_code=201)
def add_gpg_public_key(version: schemas.GPG_Public_Keys, db: Session = Depends(get_db)):
    if crud.add_gpg_public_key(db=db, version=version):
        return {"details": "201 Created"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


# response_model=schemas.Versions
@app.put("/v1/gpg-public-key/update", tags=["GPG Public Keys"])
def update_gpg_public_key_by_id(
    version: schemas.GPG_Public_Keys, db: Session = Depends(get_db)
):
    if crud.update_gpg_public_key_by_id(db=db, version=version):
        return {"details": "200 OK"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")


@app.delete("/v1/gpg-public-key/delete", tags=["GPG Public Keys"])
def delete_gpg_public_key_by_id(id: UUID4, db: Session = Depends(get_db)):
    if crud.delete_gpg_public_key_by_id(db=db, id=id):
        return {"details": "200 OK"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")
