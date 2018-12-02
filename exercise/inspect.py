#!/usr/bin/env python3
"""
函数签名
"""

from inspect import signature


def add1(x:int, y:int, *args, **kwargs) -> int :
	return x + y


sig = signature(add1)
print('{}\n{}'.format('---'*10, sig))
print('parameters: {}'.format(sig.parameters))  # OrderedDict
print('return: {}'.format(sig.return_annotation))
print(sig.parameters['y'])
print(sig.parameters['x'].annotation)
print(sig.parameters['args'])
print(sig.parameters['args'].annotation)
print(sig.parameters['kwargs'])
print(sig.parameters['kwargs'].annotation)




