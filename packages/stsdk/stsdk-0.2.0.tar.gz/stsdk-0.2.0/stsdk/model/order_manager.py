from stsdk.api.http.oms import OMSApi
from stsdk.common.key import (
    CONTRACT_TYPE_LINEAR,
    ORDER_DIRECTION_BUY,
    ORDER_DIRECTION_SELL,
    ORDER_TYPE_LIMIT,
    POSITION_SIDE_NOTBOTH,
    TIME_IN_FORCE_GTC,
)


class OrderManager:
    def __init__(self, strategy_id, account_id):
        self.omsApi = OMSApi()
        self.openOrders = dict()
        self.strategy_id = strategy_id
        self.account_id = account_id

    def place_order(self, instrument_id, price, size, side):
        data = {
            "strategy_id": self.strategy_id,
            "account_id": self.account_id,
            "quantity": size,
            "price": price,
            "instrument_id": instrument_id,
            "position_side": POSITION_SIDE_NOTBOTH,
            "contract_type": CONTRACT_TYPE_LINEAR,
            "order_type": ORDER_TYPE_LIMIT,
            "order_direction": ORDER_DIRECTION_BUY
            if side == "buy"
            else ORDER_DIRECTION_SELL,
            "time_in_force": TIME_IN_FORCE_GTC,
        }
        resp = self.omsApi.place_order(data)
        self.append_order(instrument_id, resp)
        return resp

    def cancel_order(self, instrument_id, order_id):
        data = {
            "order_id": order_id,
            "instrument_id": instrument_id,
        }
        resp = self.omsApi.cancel_order(data)
        self.remove_order(instrument_id, order_id)
        return resp

    def cancel_best_price_order(self, instrument_id, side):
        orders = {
            order_id: order_details["price"]
            for order_id, order_details in self.openOrders[instrument_id].items()
            if order_details["side"] == side
        }
        return self.cancel_order(instrument_id, max(orders, key=orders.get))

    def cancel_worst_price_order(self, instrument_id, side):
        orders = {
            order_id: order_details["price"]
            for order_id, order_details in self.openOrders[instrument_id].items()
            if order_details["side"] == side
        }
        return self.cancel_order(instrument_id, min(orders, key=orders.get))

    def cancel_instrument_orders(self, instrument_id):
        resps = []
        instrument_orders = self.openOrders[instrument_id]
        for order_id in instrument_orders:
            resps.append(self.cancel_order(instrument_id, order_id))
        return resps

    def cancel_all_orders(self):
        # await self.omsApi.cancel_all_orders()
        resps = []
        for instrument_id, orders in self.openOrders.items():
            for order_id in orders.keys():
                resps.append(self.cancel_order(instrument_id, order_id))
        return resps

    def append_order(self, instrument_id, data):
        if instrument_id not in self.openOrders:
            self.openOrders[instrument_id] = {}
        if "order_id" in data:
            order_id = data["order_id"]
            self.openOrders[instrument_id][order_id] = data

    def remove_order(self, instrument_id, order_id):
        if (
            instrument_id in self.openOrders
            and order_id in self.openOrders[instrument_id]
        ):
            del self.openOrders[instrument_id][order_id]
            if len(self.openOrders[instrument_id]) == 0:
                del self.openOrders[instrument_id]
            return True

    def remove_instrument_id(self, instrument_id):
        if instrument_id in self.openOrders:
            del self.openOrders[instrument_id]

    def get_open_orders(self, instrument_id):
        return self.openOrders.get(instrument_id, {})

    def get_all_open_orders(self):
        return self.openOrders

    def get_order_by_id(self, instrument_id, order_id):
        return self.openOrders.get(instrument_id, {}).get(order_id, None)
