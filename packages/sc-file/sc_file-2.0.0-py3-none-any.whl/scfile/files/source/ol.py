from typing import List

import lz4.block

from scfile import exceptions as exc
from scfile.consts import Signature, CUBEMAP_FACES
from scfile.files.output.dds import DdsFile, DdsOutputData
from scfile.enums import ByteOrder
from scfile.enums import StructFormat as Format
from scfile.utils.ol.dxn import DxnConverter

from .base import BaseSourceFile


SUPPORTED_FORMATS = [
    b"DXT1",
    b"DXT3",
    b"DXT5",
    b"RGBA8",
    b"BGRA8",
    b"RGBA32F",
    b"DXN_XY"
]


class OlFile(BaseSourceFile):

    output = DdsFile
    signature = Signature.OL
    order = ByteOrder.BIG

    is_cubemap = False

    def to_dds(self) -> bytes:
        return self.convert()

    @property
    def data(self) -> DdsOutputData:
        return DdsOutputData(
            self.width,
            self.height,
            self.mipmap_count,
            self.linear_size,
            self.fourcc,
            self.is_cubemap,
            self.imagedata
        )

    def parse(self) -> None:
        # Read header
        self.width = self.reader.readbin(Format.U32)
        self.height = self.reader.readbin(Format.U32)
        self.mipmap_count = self.reader.readbin(Format.U32)

        # Read encrypted FourCC (dds pixel format)
        self.fourcc = self.reader.readfourcc()

        if self.fourcc not in SUPPORTED_FORMATS:
            raise exc.OlUnknownFourcc(self.path, self.fourcc.decode())

        # Read lz4 uncompressed and compressed sizes
        self._parse_sizes()

        try:
            self.texture_id = self.reader.readstring()
            self._decompress_imagedata()

        except Exception:
            raise exc.OlInvalidFormat(self.path)

        if self.is_dxn:
            self.fourcc = b"BGRA8"
            self.imagedata = DxnConverter(self.data).to_rgba()

    @property
    def linear_size(self) -> int:
        return self.uncompressed[0]

    @property
    def is_rgba(self):
        return self.fourcc in (b"RGBA8", b"BGRA8", b"RGBA32F")

    @property
    def is_dxn(self):
        return self.fourcc in (b"DXN_XY")

    def _read_sizes(self) -> List[int]:
        return [self.reader.readbin(Format.U32) for _ in range(self.mipmap_count)]

    def _parse_sizes(self) -> None:
        self.uncompressed = self._read_sizes()
        self.compressed = self._read_sizes()

    def _decompress_imagedata(self) -> None:
        imagedata = bytearray()

        for mipmap in range(self.mipmap_count):
            imagedata.extend(
                lz4.block.decompress(
                    self.reader.read(self.compressed[mipmap]),
                    self.uncompressed[mipmap]
                )
            )

        self.imagedata = bytes(imagedata)


class OlCubemapFile(OlFile):

    is_cubemap = True

    @property
    def linear_size(self) -> int:
        return 0

    def _read_sizes(self) -> List[List[int]]:
        return [
            [self.reader.readbin(Format.U32) for _ in range(CUBEMAP_FACES)]
            for _ in range(self.mipmap_count)
        ]

    def _parse_sizes(self) -> None:
        self.uncompressed = self._read_sizes()
        self.compressed = self._read_sizes()

    def _decompress_imagedata(self) -> None:
        imagedata = bytearray()

        for mipmap in range(self.mipmap_count):
            for cubemap in range(CUBEMAP_FACES):
                imagedata.extend(
                    lz4.block.decompress(
                        self.reader.read(self.compressed[mipmap][cubemap]),
                        self.uncompressed[mipmap][cubemap]
                    )
                )

        self.imagedata = bytes(imagedata)
