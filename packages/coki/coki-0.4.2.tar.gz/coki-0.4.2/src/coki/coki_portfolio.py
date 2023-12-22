import funcs
import argparse
import inspect
import time, os, sys


parser = argparse.ArgumentParser(
    description="coki es una CLI para consultar precios en cocos"
)
parser.add_argument("tipo", help="portfolio a consultar")

args = parser.parse_args()

tipo = str(args.tipo)


disponible = funcs.get_portfolio(tipo)