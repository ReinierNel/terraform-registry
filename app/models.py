from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import relationship
from .database import Base
from uuid import uuid4

"""
Provider Tables 
"""


class Provider_GPG_Public_Keys(Base):
    __tablename__ = "provider_gpg_public_key"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    key_id = Column(String, index=True)
    ascii_armor = Column(String)


class Provider_Package(Base):
    __tablename__ = "provider_package"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    filename = Column(String, index=True)
    download_url = Column(String)
    shasums_url = Column(String)
    shasums_signature_url = Column(String)
    shasum = Column(String)
    signing_keys_id = Column(
        UUID(as_uuid=True), ForeignKey("provider_gpg_public_key.id")
    )
    os = Column(String, index=True)
    arch = Column(String, index=True)
    version_id = Column(UUID(as_uuid=True), ForeignKey("provider_versions.id"))


class Provider_Versions(Base):
    __tablename__ = "provider_versions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    namespace = Column(String, index=True)
    provider = Column(String, index=True)
    version = Column(String, index=True)
    protocols = Column(String)


class Provider_Versions_SUCKS(Base):
    __tablename__ = "provider_version_SUCS"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    namespace = Column(String, index=True)
    provider = Column(String, index=True)
    version = Column(String, index=True)
    protocols = Column(String)
