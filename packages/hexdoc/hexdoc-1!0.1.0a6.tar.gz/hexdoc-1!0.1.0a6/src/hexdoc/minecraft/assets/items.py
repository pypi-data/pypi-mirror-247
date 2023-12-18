from __future__ import annotations

from typing import Any, Self

from yarl import URL

from hexdoc.core import ItemStack, ResourceLocation

from .animated import AnimatedTexture
from .textures import BaseTexture, PNGTexture

ImageTexture = PNGTexture | AnimatedTexture


# this needs to be a separate class, rather than just using ImageTexture directly,
# because the key in the lookup for SingleItemTexture is the item id, not the texture id
class SingleItemTexture(BaseTexture):
    inner: ImageTexture

    @classmethod
    def from_url(cls, url: URL, pixelated: bool) -> Self:
        return cls(
            inner=PNGTexture(url=url, pixelated=pixelated),
        )

    @classmethod
    def load_id(cls, id: ResourceLocation | ItemStack, context: dict[str, Any]):
        return super().load_id(id.id, context)

    @property
    def url(self):
        return self.inner.url


class MultiItemTexture(BaseTexture):
    inner: list[ImageTexture]
    gaslighting: bool

    @classmethod
    def from_url(cls, url: URL, pixelated: bool) -> Self:
        return cls(
            inner=[PNGTexture(url=url, pixelated=pixelated)],
            gaslighting=False,
        )

    @classmethod
    def load_id(cls, id: ResourceLocation | ItemStack, context: dict[str, Any]):
        return super().load_id(id.id, context)


ItemTexture = SingleItemTexture | MultiItemTexture
