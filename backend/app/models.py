"""Run-scoped durable data. Evaluation labels are in a restricted schema."""

from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    Text,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def uid():
    return str(uuid4())


def now():
    return datetime.now(timezone.utc)


class Run(Base):
    __tablename__ = "simulation_runs"
    id = Column(String(36), primary_key=True, default=uid)
    seed = Column(BigInteger, nullable=False)
    network_id = Column(String(64), nullable=False, default="sim-account-1")
    asset_id = Column(String(16), nullable=False, default="SIM")
    config = Column(JSON, nullable=False)
    genesis = Column(JSON, nullable=False, default=dict)
    feed_snapshot = Column(JSON, nullable=False, default=list)
    generator_version = Column(String(32), nullable=False, default="generator-v1")
    status = Column(String(16), nullable=False, default="queued")
    tx_count = Column(Integer, nullable=False, default=0)
    analyzed_count = Column(Integer, nullable=False, default=0)
    active_version = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    error = Column(Text)


class Wallet(Base):
    __tablename__ = "wallets"
    run_id = Column(String(36), ForeignKey("simulation_runs.id"), primary_key=True)
    id = Column(String(36), primary_key=True)
    address = Column(String(64), nullable=False)
    balance_base = Column(Numeric(78, 0), nullable=False)
    next_nonce = Column(BigInteger, nullable=False, default=0)
    is_system = Column(Boolean, nullable=False, default=False)
    __table_args__ = (
        UniqueConstraint("run_id", "address"),
        CheckConstraint("balance_base >= 0"),
        CheckConstraint("next_nonce >= 0"),
    )


class Block(Base):
    __tablename__ = "blocks"
    run_id = Column(String(36), ForeignKey("simulation_runs.id"), primary_key=True)
    id = Column(String(36), primary_key=True)
    height = Column(BigInteger, nullable=False)
    block_hash = Column(String(64), nullable=False)
    parent_id = Column(String(36))
    timestamp = Column(DateTime(timezone=True), nullable=False)
    payload = Column(JSON, nullable=False)
    __table_args__ = (
        UniqueConstraint("run_id", "height"),
        UniqueConstraint("run_id", "block_hash"),
        ForeignKeyConstraint(["run_id", "parent_id"], ["blocks.run_id", "blocks.id"]),
        CheckConstraint("height >= 0"),
    )


class Transaction(Base):
    __tablename__ = "transactions"
    run_id = Column(String(36), ForeignKey("simulation_runs.id"), primary_key=True)
    id = Column(String(36), primary_key=True)
    tx_hash = Column(String(64), nullable=False)
    block_id = Column(String(36), nullable=False)
    global_index = Column(Integer, nullable=False)
    block_height = Column(BigInteger, nullable=False)
    tx_index = Column(Integer, nullable=False)
    from_wallet_id = Column(String(36), nullable=False)
    to_wallet_id = Column(String(36), nullable=False)
    from_address = Column(String(64), nullable=False)
    to_address = Column(String(64), nullable=False)
    value_base = Column(Numeric(78, 0), nullable=False)
    fee_base = Column(Numeric(78, 0), nullable=False)
    nonce = Column(BigInteger, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    payload = Column(JSON, nullable=False)
    __table_args__ = (
        UniqueConstraint("run_id", "tx_hash"),
        UniqueConstraint("run_id", "global_index"),
        UniqueConstraint("run_id", "block_id", "tx_index"),
        UniqueConstraint("run_id", "from_wallet_id", "nonce"),
        ForeignKeyConstraint(["run_id", "block_id"], ["blocks.run_id", "blocks.id"]),
        ForeignKeyConstraint(["run_id", "from_wallet_id"], ["wallets.run_id", "wallets.id"]),
        ForeignKeyConstraint(["run_id", "to_wallet_id"], ["wallets.run_id", "wallets.id"]),
        CheckConstraint("value_base > 0 AND fee_base >= 0 AND nonce >= 0 AND tx_index >= 0"),
        Index("ix_tx_sender_time", "run_id", "from_address", "timestamp"),
        Index("ix_tx_recipient_time", "run_id", "to_address", "timestamp"),
    )


class Assessment(Base):
    __tablename__ = "risk_assessments"
    run_id = Column(String(36), primary_key=True)
    tx_hash = Column(String(64), primary_key=True)
    analysis_version = Column(String(128), primary_key=True)
    as_of_order = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)
    payload = Column(JSON, nullable=False)
    __table_args__ = (
        ForeignKeyConstraint(["run_id", "tx_hash"], ["transactions.run_id", "transactions.tx_hash"]),
        CheckConstraint("score BETWEEN 0 AND 100"),
    )


class Alert(Base):
    __tablename__ = "risk_alerts"
    run_id = Column(String(36), primary_key=True)
    id = Column(String(36), primary_key=True, default=uid)
    trigger_tx_hash = Column(String(64), nullable=False)
    detector_code = Column(String(32), nullable=False)
    anchor = Column(String(256), nullable=False)
    analysis_version = Column(String(128), nullable=False)
    dedup_key = Column(String(64), nullable=False)
    score = Column(Integer, nullable=False)
    severity = Column(String(16), nullable=False)
    status = Column(String(16), nullable=False, default="open")
    revision = Column(Integer, nullable=False, default=0)
    detected_order = Column(Integer, nullable=False)
    detected_at = Column(DateTime(timezone=True), nullable=False)
    last_detected_at = Column(DateTime(timezone=True), nullable=False)
    payload = Column(JSON, nullable=False)
    __table_args__ = (
        UniqueConstraint("run_id", "dedup_key"),
        ForeignKeyConstraint(["run_id", "trigger_tx_hash"], ["transactions.run_id", "transactions.tx_hash"]),
        CheckConstraint("score BETWEEN 0 AND 100"),
        Index("ix_alert_scope", "run_id", "status", "severity", "detected_at"),
    )


class AlertTransaction(Base):
    __tablename__ = "alert_transactions"
    run_id = Column(String(36), primary_key=True)
    alert_id = Column(String(36), primary_key=True)
    tx_hash = Column(String(64), primary_key=True)
    path_order = Column(Integer, nullable=False)
    __table_args__ = (
        ForeignKeyConstraint(["run_id", "alert_id"], ["risk_alerts.run_id", "risk_alerts.id"]),
        ForeignKeyConstraint(["run_id", "tx_hash"], ["transactions.run_id", "transactions.tx_hash"]),
    )


class AlertSnapshot(Base):
    __tablename__ = "alert_snapshots"
    run_id = Column(String(36), primary_key=True)
    alert_id = Column(String(36), primary_key=True)
    as_of_order = Column(Integer, primary_key=True)
    payload = Column(JSON, nullable=False)
    __table_args__ = (ForeignKeyConstraint(["run_id", "alert_id"], ["risk_alerts.run_id", "risk_alerts.id"]),)


class RuleHit(Base):
    __tablename__ = "alert_rule_hits"
    run_id = Column(String(36), primary_key=True)
    alert_id = Column(String(36), primary_key=True)
    rule_code = Column(String(32), primary_key=True)
    payload = Column(JSON, nullable=False)
    __table_args__ = (ForeignKeyConstraint(["run_id", "alert_id"], ["risk_alerts.run_id", "risk_alerts.id"]),)


class Outbox(Base):
    __tablename__ = "outbox_events"
    run_id = Column(String(36), primary_key=True)
    tx_hash = Column(String(64), primary_key=True)
    analysis_version = Column(String(128), primary_key=True)
    global_index = Column(Integer, nullable=False)
    processed = Column(Boolean, nullable=False, default=False)
    __table_args__ = (
        ForeignKeyConstraint(["run_id", "tx_hash"], ["transactions.run_id", "transactions.tx_hash"]),
    )


class Checkpoint(Base):
    __tablename__ = "worker_checkpoints"
    run_id = Column(String(36), ForeignKey("simulation_runs.id"), primary_key=True)
    analysis_version = Column(String(128), primary_key=True)
    global_index = Column(Integer, nullable=False, default=-1)
    updated_at = Column(DateTime(timezone=True), default=now, nullable=False)


class Job(Base):
    __tablename__ = "jobs"
    id = Column(String(36), primary_key=True, default=uid)
    run_id = Column(String(36), ForeignKey("simulation_runs.id"), nullable=False)
    kind = Column(String(16), nullable=False)
    analysis_version = Column(String(128), nullable=False)
    config = Column(JSON, nullable=False, default=dict)
    status = Column(String(16), nullable=False, default="queued")
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    finished_at = Column(DateTime(timezone=True))
    error = Column(Text)
    idempotency_key = Column(String(192), nullable=False, unique=True)
    request_hash = Column(String(64), nullable=False)


class Feed(Base):
    __tablename__ = "blacklist_rules"
    id = Column(String(36), primary_key=True, default=uid)
    network_id = Column(String(64), nullable=False)
    address = Column(String(64), nullable=False)
    known_at = Column(DateTime(timezone=True), nullable=False)
    payload = Column(JSON, nullable=False)
    source_name = Column(String(64), nullable=False)
    list_version = Column(String(64), nullable=False)
    __table_args__ = (
        UniqueConstraint("network_id", "address", "source_name", "list_version"),
        Index("ix_feed_match", "network_id", "address", "known_at"),
    )


class Review(Base):
    __tablename__ = "analyst_reviews"
    id = Column(String(36), primary_key=True, default=uid)
    run_id = Column(String(36), nullable=False)
    alert_id = Column(String(36), nullable=False)
    username = Column(String(64), nullable=False)
    old_status = Column(String(16), nullable=False)
    status = Column(String(16), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    __table_args__ = (ForeignKeyConstraint(["run_id", "alert_id"], ["risk_alerts.run_id", "risk_alerts.id"]),)


class User(Base):
    __tablename__ = "users"
    username = Column(String(64), primary_key=True)
    password_hash = Column(Text, nullable=False)
    role = Column(String(16), nullable=False)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(36), ForeignKey("simulation_runs.id"))
    kind = Column(String(32), nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)


class Audit(Base):
    __tablename__ = "audit_events"
    id = Column(String(36), primary_key=True, default=uid)
    username = Column(String(64), nullable=False)
    action = Column(String(64), nullable=False)
    target = Column(String(128), nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)


class Campaign(Base):
    __tablename__ = "campaigns"
    __table_args__ = {"schema": "evaluation"}
    run_id = Column(String(36), primary_key=True)
    id = Column(String(64), primary_key=True)
    pattern = Column(String(32), nullable=False)
    tx_hashes = Column(JSON, nullable=False)


class Metric(Base):
    __tablename__ = "evaluation_metrics"
    run_id = Column(String(36), ForeignKey("simulation_runs.id"), primary_key=True)
    analysis_version = Column(String(128), primary_key=True)
    payload = Column(JSON, nullable=False)
