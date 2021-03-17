from scipy import integrate
import math

def egg_func(x):
  return x

def circle_func(x):
  return math.sqrt(1-x**2)

def main():
  print(integrate.quad(circle_func))

if __name__ == "__main__":
  main()
