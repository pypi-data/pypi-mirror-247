import funcs
import argparse
import inspect
import time, os, sys


parser = argparse.ArgumentParser(
    description="coki es una CLI para consultar precios en cocos"
)
parser.add_argument(
    "--ticker", "-T", help="Ticker a filtrar en el listado de ordenes", default="ALL"
)
parser.add_argument(
    "--filtro",
    "-F",
    help="Filtro de estado a aplicar en el listado de ordenes",
    default="cancelado",
    choices=["cancelado", "ejecutado", "mercado"],
)


parser.add_argument(
    "--refresh",
    "-R",
    help="Intervalo de actualización de los precios (en segundos)",
    default=30,
)


args = parser.parse_args()

ticker = args.ticker.upper()
filtro = args.filtro.lower()
refresh = args.refresh

# account_id = open("coki_account_id.txt", "r").read()

if refresh < 1:
    funcs.gen_table_orders(ticker=ticker, filtro=filtro)
else:
    while True:
        try:
            funcs.gen_table_orders(ticker=ticker, filtro=filtro)
            print("\n")
            time.sleep(refresh)
            os.system("cls" if os.name == "nt" else "clear")
        except KeyboardInterrupt:
            print("Saliendo...")
            sys.exit(0)
        except Exception as e:
            print(e)
            print("Error en la consulta. Intentando de nuevo...")
            time.sleep(5)
