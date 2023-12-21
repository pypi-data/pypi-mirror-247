from typing import TypeAlias, Generic, TypeVar
from dataclasses import dataclass

T = TypeVar("T")
E = TypeVar("E")


@dataclass(frozen=True)
class Some(Generic[T]):
    data: T


Option: TypeAlias = Some[T] | None


@dataclass(frozen=True)
class Ok(Generic[T]):
    ok: T


@dataclass(frozen=True)
class Err(Generic[E]):
    error: E


Result: TypeAlias = Ok[T] | Err[E]
