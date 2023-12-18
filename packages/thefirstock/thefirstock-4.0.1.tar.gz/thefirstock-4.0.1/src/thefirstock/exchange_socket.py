from thefirstock.lookUpTable.lookUpTableCreation import *


async def send_connection_key_request(userId, websocket):
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)

    connection_key_request = {
        "t": "c",
        "uid": userId,
        "actid": userId,
        "susertoken": config_data[userId]["jKey"],
        "source": "API"
    }

    await websocket.send(json.dumps(connection_key_request))

    response = await websocket.recv()
    dict_response = ast.literal_eval(response)
    if dict_response["s"] == "OK":
        print({"message": "Connection Established"})


def match_data(symbol, lookup_table):
    if symbol in lookup_table:
        return lookup_table[symbol]
    else:
        return None


async def send_continuous_feed_request(userId, websocket, list_of_symbols, callback_sub_feed=None, activate_sub_feed=False,
                                       callback_order_feed=None, activate_order_feed=False, callback_depth_feed=None,
                                       activate_depth_feed=False):
    sym = main()
    connection_string = ""

    for symbols in list_of_symbols:
        result = match_data(symbols, sym)

        if connection_string:
            connection_string = f'{connection_string}#{result["Exchange"]}|{result["Token"]}'
        else:
            connection_string = f'{result["Exchange"]}|{result["Token"]}'

    if activate_sub_feed:
        subscribe_feed = {
            "t": "t",
            "k": connection_string
        }
        await websocket.send(json.dumps(subscribe_feed))

    if activate_order_feed:
        order_feed = {
            "t": "o",
            "actid": userId
        }
        await websocket.send(json.dumps(order_feed))

    if activate_depth_feed:
        depth_feed = {
            "t": "d",
            "k": connection_string
        }
        await websocket.send(json.dumps(depth_feed))

    while True:
        feed_response = await websocket.recv()
        dict_response = ast.literal_eval(feed_response)

        if dict_response["t"] == "tk" or dict_response["t"] == "tf":
            callback_sub_feed(dict_response)

        if dict_response["t"] == "dk" or dict_response["t"] == "df":
            callback_depth_feed(dict_response)

        if dict_response["t"] == "om":
            callback_order_feed(dict_response)


async def connect_and_receive_feed(userId, symbols, socket_connection, callback_sub_feed=None, activate_sub_feed=False,
                                   callback_order_feed=None, activate_order_feed=False, callback_depth_feed=None,
                                   activate_depth_feed=False):
    conn1 = "wss://norenapi.thefirstock.com/NorenWSTP/"
    conn2 = "ws://norenapi.thefirstock.com:5810/NorenWSTP/"

    if socket_connection == 1:
        async with websockets.connect(conn1) as websocket:
            await send_connection_key_request(userId, websocket)
            await send_continuous_feed_request(userId, websocket, symbols, callback_sub_feed, activate_sub_feed,
                                               callback_order_feed, activate_order_feed, callback_depth_feed,
                                               activate_depth_feed)

    elif socket_connection == 2:
        async with websockets.connect(conn2) as websocket:
            await send_connection_key_request(userId, websocket)
            await send_continuous_feed_request(userId, websocket, symbols, callback_sub_feed, activate_sub_feed,
                                               callback_order_feed, activate_order_feed, callback_depth_feed,
                                               activate_depth_feed)


def websocket_connection(userId, sym, socket_connection, callback_sub_feed=None, activate_sub_feed=False,
                         callback_order_feed=None,
                         activate_order_feed=False, callback_depth_feed=None, activate_depth_feed=False):
    asyncio.get_event_loop().run_until_complete(
        connect_and_receive_feed(userId, sym, socket_connection, callback_sub_feed, activate_sub_feed,
                                 callback_order_feed, activate_order_feed, callback_depth_feed, activate_depth_feed))
