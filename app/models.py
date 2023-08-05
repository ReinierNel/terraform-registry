from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import relationship
from .database import Base
from uuid import uuid4


class GPG_Public_Keys(Base):
    __tablename__ = "gpg-public-key"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    key_id = Column(String, index=True)
    ascii_armor = Column(String)


class Package(Base):
    __tablename__ = "package"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    filename = Column(String, index=True)
    download_url = Column(String)
    shasums_url = Column(String)
    shasums_signature_url = Column(String)
    shasum = Column(String)
    signing_keys_id = Column(UUID(as_uuid=True), ForeignKey("gpg-public-key.id"))
    os = Column(String, index=True)
    arch = Column(String, index=True)
    version_id = Column(UUID(as_uuid=True), ForeignKey("versions.id"))


class Versions(Base):
    __tablename__ = "versions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    namespace = Column(String, index=True)
    provider = Column(String, index=True)
    version = Column(String, index=True)
    protocols = Column(String)
