from .models import ClipIn, ClipOut
from typing import Dict, Any, TypeVar, Generic, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod

M = TypeVar("M", bound=BaseModel, covariant=True)


class ToIn(Generic[M], ABC):
    def __init__(self, json: Dict[str, Any]):
        self.json = json

    @abstractmethod
    def from_version(self, version: str) -> Optional[M]:
        """
        Translate a JSON request from a past version to the current model shape.
        """
        raise NotImplementedError()


class FromOut(Generic[M], ABC):
    def __init__(self, model: M):
        self.model = model

    @abstractmethod
    def to_version(self, version: str) -> Dict[str, Any]:
        """
        Translate a response in the current model shape to a past version.
        """
        raise NotImplementedError()


# CLIP


def clip_in_2023_12_21(json: Dict[str, Any]) -> Dict[str, Any]:
    """collection -> store"""
    return {
        "store": json.get("collection", ""),
        **{k: v for k, v in json.items() if k != "collection"},
    }


def clip_in_2023_12_15(json: Dict[str, Any]) -> Dict[str, Any]:
    """multiple sibling lists -> single docs list"""
    items = []
    for i in range(0, len(json.get("texts", []))):
        item = {"text": json.get("texts", [])[i]}
        if len(json.get("ids", [])) > i:
            item["id"] = json.get("ids", [])[i]
        if len(json.get("metadatas", [])) > i:
            item["metadata"] = json.get("metadatas", [])[i]
        if len(json.get("image_urls", [])) > i:
            item["image_url"] = json.get("image_urls", [])[i]
        if json.get("embed_metadata_keys"):
            item["embed_metadata_keys"] = json.get("embed_metadata_keys")
        items.append(item)
    return {"docs": items, **{k: v for k, v in json.items() if k != "docs"}}


class ToClipIn(ToIn[ClipIn]):
    def from_version(self, version: Optional[str]) -> Optional[ClipIn]:
        versions = {
            "2023-12-15": (lambda x: clip_in_2023_12_15(x)),
            "2023-12-21": (lambda x: clip_in_2023_12_21(x)),
        }
        res = self.json
        for date, fn in sorted(versions.items(), key=lambda x: x[0]):
            if version and version < date:
                res = fn(res)
        model = None
        try:
            model = ClipIn(**res)
        except Exception as e:
            return None
        return model


def clip_out_2023_12_21(json: Dict[str, Any]) -> Dict[str, Any]:
    """metadata -> meta"""
    data = json.get("data", [])
    new_data = list(
        map(
            lambda x: {
                "meta": x.get("metadata", None),
                **{k: v for k, v in x.items() if k != "metadata"},
            },
            data,
        )
    )
    return {"data": new_data, **{k: v for k, v in json.items() if k != "data"}}


def clip_out_2023_12_15(json: Dict[str, Any]) -> Dict[str, Any]:
    """vector -> vec"""
    data = json.get("data", [])
    new_data = list(
        map(
            lambda x: {
                "vec": x.get("vector", None),
                **{k: v for k, v in x.items() if k != "vector"},
            },
            data,
        )
    )
    return {"data": new_data, **{k: v for k, v in json.items() if k != "data"}}


class FromClipOut(FromOut[ClipOut]):
    def to_version(self, version: Optional[str]) -> Dict[str, Any]:
        versions = {
            "2023-12-15": (lambda x: clip_out_2023_12_15(x)),
            "2023-12-21": (lambda x: clip_out_2023_12_21(x)),
        }
        res = self.model.dict(exclude_none=True)
        for date, fn in sorted(versions.items(), key=lambda x: x[0], reverse=True):
            if version and version <= date:
                res = fn(res)
        return res
