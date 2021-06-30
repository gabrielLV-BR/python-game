# Classe de Vetor de duas Dimensões
# Eu gosto de sempre criar esta classe quando eu vou
# programar algum jogo, pois ela ajuda muito para adicionar
# outras funcionalidades.

import math

class vec2:
  def __init__(self, x: float, y: float):
      self.x = x
      self.y = y
    
  # Adição

  def __add__(self, other):
    result = vec2(self.x, self.y).add(other)
    return result

  def add(self, other):
    self.x += other.x
    self.y += other.y

  # Subtração

  def __sub__(self, other):
    result = vec2(self.x, self.y).sub(other)
    return result

  def sub(self, other):
    self.x -= other.x
    self.y -= other.y

  # Multiplicação

  def __mul__(self, n: float):
    result = vec2(self.x, self.y).mult(n)
    return result

  def mult(self, n):
    self.x *= n
    self.y *= n

  # Divisão

  def __div__(self, n: float):
    result = vec2(self.x, self.y).div(n)
    return result

  def div(self, n):
    self.x /= n
    self.y /= n

  # Outras funções importantes

  # get_mag vai nos retornar a magnitide do vetor, o que
  # é basicamente seu tamanho. Isso nos permite normalizá-lo
  # (deixá-lo num intervalo de 0 a 1) e ver seu tamanho

  def get_mag(self) -> float:
    return math.sqrt(self.get_mag_squared())

  # Essa função existe pois caso seja necessário realizar alguma
  # comparação de distâncias, não seria necessário se ter a distância
  # "real", a quadrada seria o suficiente, pois as outras distâncias
  # também seriam quadradas. Isso faz com que não seja necessário
  # chamar a função sqrt, que é um pouco lenta. 

  def get_mag_squared(self) -> float:
    return (self.x * self.x) + (self.y * self.y)

  # Utilizado para tornar a magnitude do vetor 1, porém sem alterar
  # sua rotação

  def normalize(self):
    self.div(self.get_mag())