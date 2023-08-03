from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Signing_Keys(Base):
    __tablename__ = "signing_keys"
    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    key_id = Column(String, index=True)
    ascii_armor = Column(String)

class Provider_Package(Base):
    __tablename__ = "provider_files"
    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    filename = Column(String, index=True)
    download_url = Column(String)
    shasums_url = Column(String)
    shasums_signature_url = Column(String)
    shasum = Column(String)
    signing_keys_id = Column(Integer, ForeignKey("signing_keys.id"))
    os = Column(String, index=True)
    arch = Column(String, index=True)
    version_id = Column(Integer, ForeignKey("versions.id"))

class Versions(Base):
    __tablename__ = "versions"
    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    namespace = Column(String, index=True)
    provider = Column(String, index=True)
    version = Column(String, index=True)
    protocols = Column(String)
