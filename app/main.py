from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

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

@app.get("/v1/providers/{namespace}/{provider}/versions", response_model=schemas.Versions, tags=["Provider Registry Protocol"])
def available_versions(namespace: str, provider: str, db: Session = Depends(get_db)):
    fetch = crud.get_version_namespace_provider(db=db, namespace=namespace, provider=provider)
    if fetch is None:
        raise HTTPException(status_code=404, detail="404 Not Found")
    return fetch

@app.get("/v1/providers/{namespace}/{provider}/{version}/download/{operating_system}/{architecture}", response_model=schemas.Provider_Package, tags=["Provider Registry Protocol"])
def provider_package(namespace: str, provider: str, version: str, operating_system: str, architecture: str, db: Session = Depends(get_db)):
    fetch = crud.get_provider_os_arch_version(namespace = namespace, provider = provider, version = version, operating_system = operating_system, architecture = architecture, db = db)
    if fetch is None:
        raise HTTPException(status_code=404, detail="404 Not Found")
    return fetch


# Management CURD
@app.get("/v1/versions/getall", response_model=list[schemas.Version], tags=["Management"])
def get_all_versions(db: Session = Depends(get_db)):
    return crud.get_all_versions(db = db)

@app.get("/v1/versions/get", response_model=schemas.Version, tags=["Management"])
def get_versions_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_version_by_id(db = db, id = id)

@app.post("/v1/versions/add", tags=["Management"], status_code=201)
def add_versions(version: schemas.Version, db: Session = Depends(get_db)):
    if crud.add_version(db = db, version=version):
        return {"details": "201 Created"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")

# response_model=schemas.Versions
@app.put("/v1/versions/update", tags=["Management"])
def update_versions_by_id(version: schemas.Version, db: Session = Depends(get_db)):
    if crud.update_version(db = db, version=version):
        return {"details": "200 OK"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")

@app.delete("/v1/versions/delete", tags=["Management"])
def get_versions_by_id(id: int, db: Session = Depends(get_db)):
    if crud.delete_version_by_id(db = db, id = id):
        return {"details": "200 OK"}
    raise HTTPException(status_code=500, detail="500 Internal Server Error")

