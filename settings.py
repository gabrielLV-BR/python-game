#!/usr/bin/env python
# coding: utf8

__AUTHOR__ = "Rafael Vieira Coelho"
__DATE__ = "19/05/2019"

from pygame import Color

class Settings():
	def __init__(self, _largura: int, _altura: int, _cor_fundo: Color) -> None:
		self.largura = _largura
		self.altura = _altura
		self.cor_fundo = _cor_fundo