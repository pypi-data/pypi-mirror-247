import requests
import json
import codecs
import sys, os, time
import pandas as pd
from tabulate import tabulate
from cryptography.fernet import Fernet
from datetime import datetime


def encrypt(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data)


def decrypt(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(bytes(data, encoding="utf8"))


def gen_credentials(
    user,
    password,
    key=b"DJ4hV8Bzq_UVRqtKvHbVwwlr9zJDFAhVxro0S3tE4QM=",
    path="coki_credentials.txt",
):
    with open(path, "wb") as f:
        user = encrypt(str(user).encode(), key)
        password = encrypt(str(password).encode(), key)
        f.writelines([user, b"\n", password])


def read_credentials(
    key=b"DJ4hV8Bzq_UVRqtKvHbVwwlr9zJDFAhVxro0S3tE4QM=", path="coki_credentials.txt"
) -> (str, str):
    with open(path, "r", encoding="utf8") as f:
        user, password = f.readlines()
        user = user.strip()

    return decrypt(user, key).decode(), decrypt(password, key).decode()


def get_access_token(
    key=b"DJ4hV8Bzq_UVRqtKvHbVwwlr9zJDFAhVxro0S3tE4QM=",
    credentials_path="coki_credentials.txt",
) -> str:
    headers = {
        "authority": "api.cocos.capital",
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJhdWRpZW5jZSI6ICJjb2NvcyIsCiAgICAiaXNzIjogInN1cGFiYXNlIiwKICAgICJpYXQiOiAxNjQxOTU2NDAwLAogICAgImV4cCI6IDM5NDgzNDE1MzEKfQ.Q5ZiL7KCUKP7iSM_LHWd3gffZ0k5Ce6CemOX9CUfEdM",
        "origin": "https://app.cocos.capital",
        "referer": "https://app.cocos.capital/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
    }
    user, password = read_credentials(key, credentials_path)
    data = json.dumps({"email": user, "password": password})
    r = requests.post(
        "https://api.cocos.capital/auth/v1/token?grant_type=password",
        headers=headers,
        data=data,
    )
    s = r.content.decode("utf-8")
    with open("coki_token.txt", "w") as f:
        f.write(json.loads(s)["access_token"])
    return json.loads(s)["access_token"]


# def get_account_id(token):
#     if os.path.exists("coki_token.txt"):
#         token = open("coki_token.txt", "r").read()
#         r = requests.get(
#             "https://api.cocos.capital/api/v1/users/me",
#             headers=parse_headers_no_id(token),
#         )
#         if r.status_code == 200:
#             j = r.json()
#             if j["id_accounts"] is not None:
#                 with open("coki_account_id.txt", "w") as f:
#                     f.write(str(j["id_accounts"][0]))
#                 return j["id_accounts"][0]
#         else:
#             token = get_access_token()
#             r = requests.get(
#                 "https://api.cocos.capital/api/v1/users/me",
#                 headers=parse_headers_no_id(token),
#             )
#             if r.status_code == 200:
#                 j = r.json()
#                 if j["id_accounts"] is not None:
#                     with open("coki_account_id.txt", "w") as f:
#                         f.write(str(j["id_accounts"][0]))
#                     return j["id_accounts"][0]
#             else:
#                 print(r.content)
#                 raise Exception("Error en la consulta")
#     else:
#         token = get_access_token()
#         r = requests.get(
#             "https://api.cocos.capital/api/v1/users/me",
#             headers=parse_headers_no_id(token),
#         )
#         if r.status_code == 200:
#             j = r.json()
#             if j["id_accounts"] is not None:
#                 with open("coki_account_id.txt", "w") as f:
#                     f.write(str(j["id_accounts"][0]))
#                 return j["id_accounts"][0]
#         else:
#             print(r.content)
#             raise Exception("Error en la consulta")


def parse_headers_no_id(token):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "es-ES,es;q=0.9",
        "authorization": f"Bearer {token}",
        "if-none-match": 'W/"42-WJmuy/h7CrOCewTOtVPh5zV6UTY"',
        "recaptcha-token": "undefined",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
    }
    return headers


def parse_headers_id(token, account_id):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "es-ES,es;q=0.9",
        "authorization": f"Bearer {token}",
        "if-none-match": 'W/"42-WJmuy/h7CrOCewTOtVPh5zV6UTY"',
        "recaptcha-token": "undefined",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-account-id": str(account_id),
    }
    return headers


# Pasar autentificacion como archivo
# def get_ticker_data(ticker: str, currency: str = "AUTO", plazo=48):
#     plazo_conversion = {"48": "0003", "24": "0002", "CI": "0001", "C.I.": "0001"}
#     liquidacion_str = plazo_conversion[str(plazo).upper()]

#     if (
#         currency == "AUTO"
#     ):  # Si currency es auto, pasa a usd si termina en D o C (para casos como AMD, no va a andar auto, hay que poner currency ARS)
#         if ticker[-1] in ["D", "C"]:
#             currency = "USD"
#             ticker = ticker[:-1]
#         else:
#             currency = "ARS"

#     currency = "USD" if currency == "D" else currency
#     species = "D" if currency == "USD" else ""
#     link = f"https://api.cocos.capital/api/v1/markets/ticker/{ticker}{species}-{liquidacion_str}-C-CT-{currency}"

#     #### TODO: adaptar esto a una funcion generica, que sea "crear token si no existe o no anda, sino usar el que esta"

#     if os.path.exists("coki_token.txt"):
#         token = open("coki_token.txt", "r").read()
#         if not os.path.exists("coki_account_id.txt"):
#             account_id = get_account_id(token)
#         else:
#             account_id = open("coki_account_id.txt", "r").read()

#         r = requests.get(link, headers=parse_headers_id(token, account_id))
#         if r.status_code == 200:
#             j = r.json()
#             if j["bids"] is not None:
#                 return j
#         else:
#             token = get_access_token()
#             if not os.path.exists("coki_account_id.txt"):
#                 account_id = get_account_id(token)
#             else:
#                 account_id = open("coki_account_id.txt", "r").read()
#             r = requests.get(link, headers=parse_headers_id(token, account_id))
#             if r.status_code == 200:
#                 j = r.json()
#                 if j["bids"] is not None:
#                     return j
#             else:
#                 print(r.content)
#                 raise Exception("Error en la consulta")
#     else:
#         token = get_access_token()
#         if not os.path.exists("coki_account_id.txt"):
#             account_id = get_account_id(token)
#         else:
#             account_id = open("coki_account_id.txt", "r").read()
#         r = requests.get(link, headers=parse_headers_id(token, account_id))
#         if r.status_code == 200:
#             j = r.json()
#             if j["bids"] is not None:
#                 return j
#         else:
#             print(r.content)
#             raise Exception("Error en la consulta")


# def gen_table(ticker: str, currency: str = "AUTO", plazo=48):
#     data = get_ticker_data(ticker, currency, plazo)

#     compra_size = []
#     compra_price = []
#     for row in data["bids"]:
#         compra_size.append(row["size"])
#         compra_price.append(row["price"])

#     venta_size = []
#     venta_price = []
#     for row in data["asks"]:
#         venta_size.append(row["size"])
#         venta_price.append(row["price"])

#     table = {
#         "Cant. compra": compra_size,
#         "Precio compra": compra_price,
#         "": "",
#         "Precio venta": venta_price,
#         "Cant. venta": venta_size,
#     }
#     time_str = datetime.now().strftime("%H:%M:%S")

#     print(
#         "\t",
#         data["short_ticker"],
#         "-",
#         data["instrument_name"],
#         "-",
#         data["currency"],
#         "-",
#         time_str,
#     )

#     for var in ["last", "high", "low", "volume"]:
#         if data[var] == None:
#             data[var] = "---"

#     print(
#         "\t",
#         f'Last: {data["last"]} - High: {data["high"]} - Low: {data["low"]} - Volume: {data["volume"]}',
#     )

#     print(
#         tabulate(
#             table,
#             headers="keys",
#             tablefmt="rounded_outline",
#             floatfmt=".2f",
#             stralign="center",
#         )
#     )


def screener(ticker, currency, plazo, refresh):
    while True:
        try:
            gen_table(ticker, currency, plazo)
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


def get_orders_link():
    link = "https://api.cocos.capital/api/v2/orders/"

    token = token_promise()
    account_id = account_promise(token)
    headers = parse_headers_id(token, account_id)

    orders = requests.request("GET", link, headers=headers)

    # print(response.text)
    # orders es una lista donde cada elemento es un diccionario con los datos de cada orden
    return orders.json()


def gen_table_orders(ticker="ALL", filtro="cancelado"):
    orders = get_orders_link()

    tables = []
    for i, item in enumerate(orders):
        data = orders[i]

        if data["currency"] == "USD":
            ticker_name = data["ticker"] + "D"
        else:
            ticker_name = data["ticker"]

        if data["status"] == "MARKET":
            ejecutadas = 0
        else:
            ejecutadas = data["result_quantity"]
        table = {
            "Hora": datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%S.%f%z")
            .time()
            .strftime("%H:%M"),
            "Ticker": ticker_name,
            "Estado": data["status"],
            "Operación": data["order_type"],
            "Precio": round(data["set_price"], 2),
            "Cantidad": int(round(data["set_quantity"], 0)),
            "Monto": int(round(data["set_amount"], 2)),
            "Ejecutadas": ejecutadas,
            "code_op": data["order_id"],
        }
        tables.append(table)

    df = pd.DataFrame(tables)
    df = df.copy().sort_values(by=["Hora"], ascending=True).reset_index(drop=True)
    df["Op"] = df.index
    df = df.copy().set_index("Op")

    df["Estado"] = df["Estado"].replace(
        {
            "MARKET": "En mercado",
            "CANCELLED": "Cancelada",
            "REJECTED": "Rechazada",
            "EXECUTED": "Ejecutada",
            "PARTIALLY_EXECUTED": "Ejecutada parcialmente",
        }
    )

    if filtro == "cancelado":
        df = df[(df["Estado"] != "Cancelada") & (df["Estado"] != "Rechazada")].copy()
    elif filtro == "ejecutado":
        df = df[df["Estado"] == "Ejecutada"].copy()
    elif filtro == "mercado":
        df = df[
            (df["Estado"] == "Ejecutada parcialmente") | (df["Estado"] == "En mercado")
        ].copy()

    df["Operación"] = df["Operación"].replace(
        {
            "BUY": "Compra",
            "SELL": "Venta",
        }
    )

    if ticker != "ALL":
        df = df[df["Ticker"] == ticker].copy()

    df = df.sort_values(by=["Ticker", "Hora"], ascending=False)

    dict_operaciones = df["code_op"].to_dict()

    time_str = datetime.now().strftime("%H:%M:%S")

    mail = read_credentials()[0]

    print("\n \t \t \t", "Actualizado a:", time_str, "-", " Cuenta:", mail, "\n")

    print(
        tabulate(
            df[df.columns[:-1]],
            headers="keys",
            tablefmt="rounded_outline",
            floatfmt=".2f",
            stralign="center",
        )
    )
    return dict_operaciones


def request_info(link, token, account_id=None, info_type="ticker", payload={}):
    if info_type == "ticker":
        r = requests.get(link, headers=parse_headers_id(token, account_id))
    elif info_type == "account":
        r = requests.get(
            link,
            headers=parse_headers_no_id(token),
        )
    elif info_type == "wallet":
        r = requests.get(
            link,
            headers=parse_headers_id(token, account_id),
        )
    elif info_type == "place_order":
        r = requests.post(
            link, headers=parse_headers_id(token, account_id), json=payload
        )
    elif info_type == "cancel_order":
        r = requests.delete(link, headers=parse_headers_id(token, account_id))

    if r.status_code == 200:
        j = r.json()
        if not "success" in j.keys():
            return j
        if (j["success"] != False) or (j["success"] != "false"):
            return j
    else:
        sys.tracebacklimit = 0
        error = r.content.decode("utf-8")
        raise Exception(f"Error en la consulta: {error}")


def get_account_id(token):
    link = "https://api.cocos.capital/api/v1/users/me"

    j = request_info(link, token, info_type="account")

    if j["id_accounts"] is not None:
        with open("coki_account_id.txt", "w") as f:
            f.write(str(j["id_accounts"][0]))
        return j["id_accounts"][0]
    else:
        raise Exception("Error en la consulta")


def token_promise():
    if os.path.exists("coki_token.txt"):
        token = open("coki_token.txt", "r").read()
        r = requests.get(
            "https://api.cocos.capital/api/v1/users/me",
            headers=parse_headers_no_id(token),
        )
        if r.status_code == 200:
            pass
        else:
            token = get_access_token()
    else:
        token = get_access_token()
    return token


def account_promise(token):
    if os.path.exists("coki_account_id.txt"):
        account_id = open("coki_account_id.txt", "r").read()
    else:
        account_id = get_account_id(token)

    return account_id


def get_ticker_data(ticker: str, currency: str = "AUTO", plazo=48):
    plazo_conversion = {"48": "0003", "24": "0002", "CI": "0001", "C.I.": "0001"}
    liquidacion_str = plazo_conversion[str(plazo).upper()]

    if (
        currency == "AUTO"
    ):  # Si currency es auto, pasa a usd si termina en D o C (para casos como AMD, no va a andar auto, hay que poner currency ARS)
        if ticker[-1] in ["D", "C"]:
            currency = "USD"
            ticker = ticker[:-1]
        else:
            currency = "ARS"

    currency = "USD" if currency == "D" else currency
    species = "D" if currency == "USD" else ""
    link = f"https://api.cocos.capital/api/v1/markets/ticker/{ticker}{species}-{liquidacion_str}-C-CT-{currency}"

    token = token_promise()
    account_id = account_promise(token)

    ticker_link = f"{ticker}{species}-{liquidacion_str}-C-CT-{currency}"

    j = request_info(link, token, account_id)
    if j["bids"] is not None:
        return j, ticker_link
    else:
        raise Exception("Error en la consulta")


def gen_table(ticker: str, currency: str = "AUTO", plazo=48):
    data, ticker_link = get_ticker_data(ticker, currency, plazo)

    compra_size = []
    compra_price = []
    for row in data["bids"]:
        compra_size.append(row["size"])
        compra_price.append(row["price"])

    venta_size = []
    venta_price = []
    for row in data["asks"]:
        venta_size.append(row["size"])
        venta_price.append(row["price"])

    table = {
        "Cant. compra": compra_size,
        "Precio compra": compra_price,
        "": "",
        "Precio venta": venta_price,
        "Cant. venta": venta_size,
    }
    time_str = datetime.now().strftime("%H:%M:%S")

    print(
        "\t",
        data["short_ticker"],
        "-",
        data["instrument_name"],
        "-",
        data["currency"],
        "-",
        time_str,
    )

    for var in ["last", "high", "low", "volume"]:
        if data[var] == None:
            data[var] = "---"

    print(
        "\t",
        f'Last: {data["last"]} - High: {data["high"]} - Low: {data["low"]} - Volume: {data["volume"]}',
    )

    print(
        tabulate(
            table,
            headers="keys",
            tablefmt="rounded_outline",
            floatfmt=".2f",
            stralign="center",
        )
    )
    return (
        data,
        ticker_link,
    )  # FIXME: el ticker link lo puedo sacar directamente de data (data['long_ticker']). No deberia ser necesario devolverlo aparte, pero quizas es un bardo cambiarlo


def get_portfolio(op_type="all"):
    link = f"https://api.cocos.capital/api/v1/wallet/portfolio"

    token = token_promise()
    account_id = account_promise(token)

    j = request_info(link, token, account_id, info_type="wallet")

    time_str = datetime.now().strftime("%H:%M:%S")

    mail = read_credentials()[0]

    # disponible = {'Total en Pesos': j['total']['ars'], 'Total en Dolares': j['total']['usd']}
    portfolio = j["tickers"]

    tables = []
    for i in range(0, len(portfolio)):
        data = portfolio[i]

        table = {
            "Ticker": data["ticker"],
            "Cantidad": data["quantity"],
        }
        tables.append(table)
    df = pd.DataFrame(tables)
    df = df.copy().set_index("Ticker")

    if op_type == "all":
        print(
            "\n",
            time_str,
            "\n",
            mail,
            "\n",
            # f'Porfolio total en ARS: $ {int(j["total"]["ars"]):,}',
            # "\n",
            # f'Porfolio total en USD: $ {int(j["total"]["usd"]):,}',
        )
        print(
            tabulate(
                df,
                headers="keys",
                tablefmt="rounded_outline",
                floatfmt=".0f",
                stralign="center",
            )
        )
    if op_type == "buy":
        print(
            "\n",
            time_str,
            "\n",
            mail,
            "\n",
            # f'Porfolio total en ARS: $ {int(j["total"]["ars"]):,}',
            # "\n",
            # f'Porfolio total en USD: $ {int(j["total"]["usd"]):,}',
        )
        print(
            tabulate(
                df.iloc[:2],
                headers="keys",
                tablefmt="rounded_outline",
                floatfmt=".0f",
                stralign="center",
            )
        )
    if op_type == "sell":
        print(
            "\n",
            time_str,
            "\n",
            mail,
            "\n",
            # f'Porfolio total en ARS: $ {int(j["total"]["ars"]):,}',
            # "\n",
            # f'Porfolio total en USD: $ {int(j["total"]["usd"]):,}',
        )
        print(
            tabulate(
                df.iloc[2:],
                headers="keys",
                tablefmt="rounded_outline",
                floatfmt=".0f",
                stralign="center",
            )
        )

    d = df.iloc[:2].to_dict("index")
    return (d["AR$"]["Cantidad"], d["US$ MEP"]["Cantidad"])


def calcula_operaciones(
    cantidad: str, disponible: tuple, precio: float, currency: str, data: dict
):
    """
    Calcula el numero de acciones a comprar o vender
    """

    if cantidad == "a":
        if currency == "USD":
            acciones = int(disponible[1] / precio)
        elif currency == "ARS":
            acciones = int(disponible[0] / precio)
    elif cantidad[-1] == "a":
        acciones = int(cantidad[:-1])
    elif cantidad[-1] == "%":
        if currency == "USD":
            acciones = int(disponible[1] * int(cantidad[:-1]) / 100 / precio)
        elif currency == "ARS":
            acciones = int(disponible[0] * int(cantidad[:-1]) / 100 / precio)
    elif cantidad[-1] not in ["a", "%"]:
        acciones = int(int(cantidad) / precio)

    assert acciones > 0, "No se puede operar con esa cantidad"
    if currency == "USD":
        assert (
            acciones * precio < disponible[1]
        ), f"No hay suficiente dinero para operar - Disponible: {round(disponible[1],2)}"
    elif currency == "ARS":
        assert (
            acciones * precio < disponible[0]
        ), f"No hay suficiente dinero para operar - Disponible: {round(disponible[0],2)}"

    tick_size = data["tick_size"]
    assert (
        precio / tick_size
    ).is_integer(), f'El precio no es multiplo de ({data["tick_size"]})'

    if precio > data["last"] * 1.05:
        correct = input(
            f'El precio elegido es un 5% mayor al último operado ({data["last"]}). ¿Es correcto? (S/N): '
        )
        while correct not in ["S", "N", "s", "n"]:
            correct = input(
                f'El precio elegido es un 5% mayor al último operado ({data["last"]}). ¿Es correcto? (S/N): '
            )
        if correct in ["N", "n"]:
            raise ValueError("Precio incorrecto")

    elif precio < data["last"] * 0.95:
        correct = input(
            f'El precio elegido es más que 5% menor al último operado ({data["last"]}). ¿Es correcto? (S/N): '
        )
        while correct not in ["S", "N", "s", "n"]:
            correct = input(
                f'El precio elegido es más que 5% menor al último operado ({data["last"]}). ¿Es correcto? (S/N): '
            )
        if correct in ["N", "n"]:
            raise ValueError("Precio incorrecto")

    return acciones


def place_order(side, long_ticker, quantity, price, order_type="limit"):
    """Ejecuta la orden en el mercado, en teoría ya verificados"""
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("side must be BUY or SELL")
    if order_type.upper() not in ["LIMIT", "MARKET"]:
        raise ValueError("order_type must be LIMIT or MARKET")

    payload = {
        "long_ticker": long_ticker,
        "price": float(price),
        "quantity": int(quantity),
        "side": side.upper(),
        "type": order_type.upper(),
    }

    token = token_promise()
    account_id = account_promise(token)

    link = "https://api.cocos.capital/api/v2/orders/"

    result = request_info(link, token, account_id, "place_order", payload)
    return result
