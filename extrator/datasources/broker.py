"""Descritivo das interfaces para postar nas filas de processamento de inteiro teores"""

from ..settings import celeryapp

@celeryapp.task(name='zuleika.classificar')
def classificar(id, texto):
    pass
