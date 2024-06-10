#!/usr/bin/env python3
"""
Created on 2024-06-10 (Mon) 23:13:47

@author: I.Azuma
"""
import math

def calculation_circle(diameter):
	try:
		diameter = int(diameter)
		#半径
		radius = diameter / 2
		#面積
		area = radius * radius * math.pi
		#円周
		circumference = diameter * math.pi
		
		return area, circumference
	except :
		return '数値を入力してください'
