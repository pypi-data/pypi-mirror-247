import funcs
import argparse
import inspect
import time, os, sys


parser = argparse.ArgumentParser(
    description="coki es una CLI para consultar precios en cocos"
)
parser.add_argument("ticker", help="Ticker a consultar")
parser.add_argument(
    "--currency",
    "-C",
    help="Moneda del ticker. Por default lo infiere de la última letra del Ticker (pero va a fallar en casos como AMD)",
    default="auto",
)

parser.add_argument("--plazo", "-P", help="Plazo de la operación", default=48)

args = parser.parse_args()

ticker = args.ticker.upper()
currency = args.currency.upper()

disponible = funcs.get_portfolio(op_type="buy")

data, ticker_link = funcs.gen_table(ticker, currency, args.plazo)

if (
    currency == "AUTO"
):  # Si currency es auto, pasa a usd si termina en D o C (para casos como AMD, no va a andar auto, hay que poner currency ARS)
    if ticker[-1] in ["D", "C"]:
        currency = "USD"
        ticker = ticker[:-1]
    else:
        currency = "ARS"

precio = float(input("Precio: "))
cantidad = str(input("Invertir (h para ayuda): "))
while cantidad == "h":
    print(
        """Este parámetro permite definir la cantidad de acciones, cantidad de dinero, o el porcentaje del portfolio a invertir. Ejemplos:
          10a: Compra 10 acciones
          10%: Compra el 10% del portfolio
          10: Compra 10 dólares/pesos en acciones
          a: todo el capital disponible"""
    )
    cantidad = str(input("Invertir (h para ayuda): "))

acciones = funcs.calcula_operaciones(cantidad, disponible, precio, currency, data)

# Verificación final

verificacion = ""

while verificacion not in ["S", "N", "s", "n"]:
    verificacion = input(
        f"""---------------- 
Ticker: {ticker}
Cantidad: {acciones}
Precio: {precio} 
Monto de la operación: {acciones*precio}
----------------
¿Confirmas la operación? (S/N)"""
    )

if verificacion in ["S", "s"]:
    print("Enviando orden...")
    funcs.place_order(
        side="BUY",
        long_ticker=ticker_link,
        quantity=acciones,
        price=precio,
        order_type="limit",
    )
elif verificacion in ["N", "n"]:
    print("Cancelando orden...")
