#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2023-06-06
"""

import torch

from ..common import AbstractTransform

__all__ = [
    'OCR',
]


# TODO 换个ocr源
class OCR(AbstractTransform):

    def __init__(self, lang: str = 'ch_sim') -> None:
        """OCR, 光学字符识别

        Args:
            lang: Language codes, 识别语言, {"ch_sim", "en", "ko", "ja"}, "ch_sim"
        """
        super().__init__(use_gpu=True)

        try:
            import easyocr
        except ImportError:
            raise RuntimeError(
                'The OCR module requires "easyocr" package. '
                'You should install it by "pip install easyocr".'
            )
        self.reader = easyocr.Reader([lang], gpu=True)

    def _apply(self, sample):

        if sample.image is None:
            return sample

        image = sample.image.transpose(0, 2).transpose(0, 1)
        image = image.type(torch.uint8).cpu().numpy()
        sample.ocr = self.reader.readtext(image)

        return sample
