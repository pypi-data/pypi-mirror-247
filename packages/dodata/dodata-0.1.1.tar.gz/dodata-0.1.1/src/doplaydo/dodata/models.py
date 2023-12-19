# ruff: noqa: UP007, D101, E501
"""Defines SQLAlchemy models and tables for everything in dodata.

Please refrain from adding special methods directly to the models. Strive for:
    models.py:
        class MyModel(SQLModel):

    mymodel.py:
        def special_method(obj):
            ...
"""
from datetime import datetime
from enum import StrEnum
from sqlalchemy import CheckConstraint, JSON
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlmodel import Column, Field, Relationship, SQLModel, UniqueConstraint
from typing import Optional

JSON_VARIANT = JSONB().with_variant(JSON(), "sqlite")


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    suffix: str = Field(index=True)
    description: Optional[str]
    timestamp: datetime = Field(default=datetime.utcnow(), index=True)
    cells: list["Cell"] = Relationship(
        back_populates="project", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    wafers: list["Wafer"] = Relationship(
        back_populates="project", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Cell(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("project_id", "name", name="unique_name_and_project_on_cell"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    attributes: dict = Field(sa_column=Column(JSON_VARIANT), default={})
    project_id: int = Field(foreign_key="project.id")
    project: Project = Relationship(back_populates="cells")
    timestamp: datetime = Field(default=datetime.utcnow(), index=True)
    devices: list["Device"] = Relationship(
        back_populates="cell",
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "foreign_keys": "Device.cell_id",
        },
    )


class Device(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "x",
            "y",
            "angle",
            "mirror",
            "parent_cell_id",
            "cell_id",
            name="unique_coord_cells_on_device",
        ),
        UniqueConstraint("cell_id", "name", name="unique_device_names_per_cell"),
        CheckConstraint(
            "parent_cell_id <> cell_id", name="unique_device_cell_references"
        ),
        CheckConstraint(
            "(parent_cell_id IS NULL and x IS NULL and y IS NULL and angle is NULL and mirror is NULL)"
            " OR "
            "(parent_cell_id IS NOT NULL and x IS NOT NULL and y IS NOT NULL and angle IS NOT NULL and mirror IS NOT NULL)",
            name="parent_cell_coordinate_reference_not_null",
        ),
        CheckConstraint(
            "parent_cell_id <> cell_id", name="unique_device_cell_references"
        ),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    cell: Cell = Relationship(
        back_populates="devices",
        sa_relationship_kwargs={"foreign_keys": "Device.cell_id"},
    )
    cell_id: int = Field(foreign_key="cell.id")
    name: str = Field(index=True)
    attributes: dict = Field(sa_column=Column(JSON_VARIANT), default={})
    x: Optional[float] = Field(default=None, index=True)
    y: Optional[float] = Field(default=None, index=True)
    angle: Optional[float] = Field(default=None, index=True)
    mirror: Optional[bool] = Field(default=None, index=True)
    parent_cell: Optional[Cell] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Device.parent_cell_id"}
    )
    parent_cell_id: Optional[int] = Field(
        default=None, foreign_key="cell.id", nullable=True
    )
    timestamp: datetime = Field(default=datetime.utcnow(), index=True)
    device_data: list["DeviceData"] = Relationship(
        back_populates="device", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Wafer(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("project_id", "name", name="unique_wafer_name_per_project"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str]
    lot_name: Optional[str] = Field(default=None, index=True)
    attributes: dict = Field(sa_column=Column(JSON_VARIANT), default={})
    timestamp: datetime = Field(default=datetime.utcnow(), index=True)
    project_id: int = Field(foreign_key="project.id")
    project: Project = Relationship(back_populates="wafers")
    dies: list["Die"] = Relationship(
        back_populates="wafer", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    analysis: list["Analysis"] = Relationship(
        back_populates="wafer", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Die(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("x", "y", "wafer_id", name="unique_wafer_die"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    x: int = Field(index=True)
    y: int = Field(index=True)
    attributes: dict = Field(sa_column=Column(JSON_VARIANT), default={})
    wafer_id: int = Field(foreign_key="wafer.id")
    wafer: Wafer = Relationship(back_populates="dies")
    timestamp: datetime = Field(default=datetime.utcnow(), index=True)
    device_data: list["DeviceData"] = Relationship(
        back_populates="die", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    analysis: list["Analysis"] = Relationship(
        back_populates="die", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class DeviceDataType(StrEnum):
    simulation = "simulation"
    measurement = "measurement"


class DeviceData(SQLModel, table=True):
    __tablename__ = "device_data"
    id: Optional[int] = Field(default=None, primary_key=True)
    data_type: DeviceDataType = Field(index=True)
    path: str
    thumbnail_path: Optional[str] = Field(default=None)
    attributes: dict = Field(sa_column=Column(JSON_VARIANT), default={})
    plotting_kwargs: dict = Field(sa_column=Column(JSON_VARIANT), default=None)
    is_bad: bool = Field(default=False, index=True)
    device: Device = Relationship(back_populates="device_data")
    device_id: int = Field(foreign_key="device.id", nullable=True)
    die_id: Optional[int] = Field(foreign_key="die.id", nullable=True)
    die: Optional[Die] = Relationship(back_populates="device_data")
    timestamp: datetime = Field(default=datetime.utcnow(), index=True)
    analysis: list["Analysis"] = Relationship(
        back_populates="device_data", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Analysis(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint(
            "1 = (CASE WHEN device_data_id IS NOT NULL THEN 1 ELSE 0 END + \
                              CASE WHEN die_id IS NOT NULL THEN 1 ELSE 0 END + \
                              CASE WHEN wafer_id IS NOT NULL THEN 1 ELSE 0 END)",
            name="analysis_ids_xor_constraint",
        ),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default=datetime.utcnow(), index=True)
    function_name: str = Field(index=True)
    parameters: dict = Field(sa_column=Column(JSON_VARIANT))
    output: dict = Field(sa_column=Column(JSON_VARIANT))
    summary_plot: str
    attributes: dict = Field(sa_column=Column(JSON_VARIANT), default={})
    is_bad: bool = Field(default=False, index=True)
    device_data_id: Optional[int] = Field(foreign_key="device_data.id", nullable=True)
    device_data: Optional[DeviceData] = Relationship(back_populates="analysis")
    die_id: Optional[int] = Field(foreign_key="die.id", nullable=True)
    die: Optional[Die] = Relationship(back_populates="analysis")
    wafer_id: Optional[int] = Field(foreign_key="wafer.id", nullable=True)
    wafer: Optional[Wafer] = Relationship(back_populates="analysis")

    @property
    def name(self):
        """Return a name for the analysis."""
        mapping = {
            "Device Data": self.device_data_id,
            "Die": self.die_id,
            "Wafer": self.wafer_id,
        }
        model_id = f"{[ str(k) + ' #' + str(v) for k,v in mapping.items() if v][0] }"
        return f"{self.function_name} on {model_id}"
