from copy import copy
from typing import Dict, List, Set

from weathon.quantization.datamodel import ContractData, OrderData, PositionData, OrderRequest, TradeData
from weathon.quantization.utils.constants import Exchange, Direction, Offset


class PositionHolding:
    """"""

    def __init__(self, contract: ContractData) -> None:
        """"""
        self.vt_symbol: str = contract.vt_symbol
        self.exchange: Exchange = contract.exchange

        self.active_orders: Dict[str, OrderData] = {}

        self.long_pos: float = 0
        self.long_yd: float = 0
        self.long_td: float = 0

        self.short_pos: float = 0
        self.short_yd: float = 0
        self.short_td: float = 0

        self.long_pos_frozen: float = 0
        self.long_yd_frozen: float = 0
        self.long_td_frozen: float = 0

        self.short_pos_frozen: float = 0
        self.short_yd_frozen: float = 0
        self.short_td_frozen: float = 0

    def update_position(self, position: PositionData) -> None:
        """"""
        if position.direction == Direction.LONG:
            self.long_pos = position.volume
            self.long_yd = position.yd_volume
            self.long_td = self.long_pos - self.long_yd
        else:
            self.short_pos = position.volume
            self.short_yd = position.yd_volume
            self.short_td = self.short_pos - self.short_yd

    def update_order(self, order: OrderData) -> None:
        """"""
        if order.is_active():
            self.active_orders[order.vt_orderid] = order
        else:
            if order.vt_orderid in self.active_orders:
                self.active_orders.pop(order.vt_orderid)

        self.calculate_frozen()

    def update_order_request(self, req: OrderRequest, vt_orderid: str) -> None:
        """"""
        gateway_name, orderid = vt_orderid.split(".")

        order: OrderData = req.create_order_data(orderid, gateway_name)
        self.update_order(order)

    def update_trade(self, trade: TradeData) -> None:
        """"""
        if trade.direction == Direction.LONG:
            if trade.offset == Offset.OPEN:
                self.long_td += trade.volume
            elif trade.offset == Offset.CLOSETODAY:
                self.short_td -= trade.volume
            elif trade.offset == Offset.CLOSEYESTERDAY:
                self.short_yd -= trade.volume
            elif trade.offset == Offset.CLOSE:
                if trade.exchange in {Exchange.SHFE, Exchange.INE}:
                    self.short_yd -= trade.volume
                else:
                    self.short_td -= trade.volume

                    if self.short_td < 0:
                        self.short_yd += self.short_td
                        self.short_td = 0
        else:
            if trade.offset == Offset.OPEN:
                self.short_td += trade.volume
            elif trade.offset == Offset.CLOSETODAY:
                self.long_td -= trade.volume
            elif trade.offset == Offset.CLOSEYESTERDAY:
                self.long_yd -= trade.volume
            elif trade.offset == Offset.CLOSE:
                if trade.exchange in {Exchange.SHFE, Exchange.INE}:
                    self.long_yd -= trade.volume
                else:
                    self.long_td -= trade.volume

                    if self.long_td < 0:
                        self.long_yd += self.long_td
                        self.long_td = 0

        self.long_pos = self.long_td + self.long_yd
        self.short_pos = self.short_td + self.short_yd

        # Update frozen volume to ensure no more than total volume
        self.sum_pos_frozen()

    def calculate_frozen(self) -> None:
        """"""
        self.long_pos_frozen = 0
        self.long_yd_frozen = 0
        self.long_td_frozen = 0

        self.short_pos_frozen = 0
        self.short_yd_frozen = 0
        self.short_td_frozen = 0

        for order in self.active_orders.values():
            # Ignore position open orders
            if order.offset == Offset.OPEN:
                continue

            frozen: float = order.volume - order.traded

            if order.direction == Direction.LONG:
                if order.offset == Offset.CLOSETODAY:
                    self.short_td_frozen += frozen
                elif order.offset == Offset.CLOSEYESTERDAY:
                    self.short_yd_frozen += frozen
                elif order.offset == Offset.CLOSE:
                    self.short_td_frozen += frozen

                    if self.short_td_frozen > self.short_td:
                        self.short_yd_frozen += (self.short_td_frozen
                                                 - self.short_td)
                        self.short_td_frozen = self.short_td
            elif order.direction == Direction.SHORT:
                if order.offset == Offset.CLOSETODAY:
                    self.long_td_frozen += frozen
                elif order.offset == Offset.CLOSEYESTERDAY:
                    self.long_yd_frozen += frozen
                elif order.offset == Offset.CLOSE:
                    self.long_td_frozen += frozen

                    if self.long_td_frozen > self.long_td:
                        self.long_yd_frozen += (self.long_td_frozen
                                                - self.long_td)
                        self.long_td_frozen = self.long_td

        self.sum_pos_frozen()

    def sum_pos_frozen(self) -> None:
        """"""
        # Frozen volume should be no more than total volume
        self.long_td_frozen = min(self.long_td_frozen, self.long_td)
        self.long_yd_frozen = min(self.long_yd_frozen, self.long_yd)

        self.short_td_frozen = min(self.short_td_frozen, self.short_td)
        self.short_yd_frozen = min(self.short_yd_frozen, self.short_yd)

        self.long_pos_frozen = self.long_td_frozen + self.long_yd_frozen
        self.short_pos_frozen = self.short_td_frozen + self.short_yd_frozen

    def convert_order_request_shfe(self, req: OrderRequest) -> List[OrderRequest]:
        """"""
        if req.offset == Offset.OPEN:
            return [req]

        if req.direction == Direction.LONG:
            pos_available: int = self.short_pos - self.short_pos_frozen
            td_available: int = self.short_td - self.short_td_frozen
        else:
            pos_available: int = self.long_pos - self.long_pos_frozen
            td_available: int = self.long_td - self.long_td_frozen

        if req.volume > pos_available:
            return []
        elif req.volume <= td_available:
            req_td: OrderRequest = copy(req)
            req_td.offset = Offset.CLOSETODAY
            return [req_td]
        else:
            req_list: List[OrderRequest] = []

            if td_available > 0:
                req_td: OrderRequest = copy(req)
                req_td.offset = Offset.CLOSETODAY
                req_td.volume = td_available
                req_list.append(req_td)

            req_yd: OrderRequest = copy(req)
            req_yd.offset = Offset.CLOSEYESTERDAY
            req_yd.volume = req.volume - td_available
            req_list.append(req_yd)

            return req_list

    def convert_order_request_lock(self, req: OrderRequest) -> List[OrderRequest]:
        """"""
        if req.direction == Direction.LONG:
            td_volume: int = self.short_td
            yd_available: int = self.short_yd - self.short_yd_frozen
        else:
            td_volume: int = self.long_td
            yd_available: int = self.long_yd - self.long_yd_frozen

        close_yd_exchanges: Set[Exchange] = {Exchange.SHFE, Exchange.INE}

        # If there is td_volume, we can only lock position
        if td_volume and self.exchange not in close_yd_exchanges:
            req_open: OrderRequest = copy(req)
            req_open.offset = Offset.OPEN
            return [req_open]
        # If no td_volume, we close opposite yd position first
        # then open new position
        else:
            close_volume: int = min(req.volume, yd_available)
            open_volume: int = max(0, req.volume - yd_available)
            req_list: List[OrderRequest] = []

            if yd_available:
                req_yd: OrderRequest = copy(req)
                if self.exchange in close_yd_exchanges:
                    req_yd.offset = Offset.CLOSEYESTERDAY
                else:
                    req_yd.offset = Offset.CLOSE
                req_yd.volume = close_volume
                req_list.append(req_yd)

            if open_volume:
                req_open: OrderRequest = copy(req)
                req_open.offset = Offset.OPEN
                req_open.volume = open_volume
                req_list.append(req_open)

            return req_list

    def convert_order_request_net(self, req: OrderRequest) -> List[OrderRequest]:
        """"""
        if req.direction == Direction.LONG:
            pos_available: int = self.short_pos - self.short_pos_frozen
            td_available: int = self.short_td - self.short_td_frozen
            yd_available: int = self.short_yd - self.short_yd_frozen
        else:
            pos_available: int = self.long_pos - self.long_pos_frozen
            td_available: int = self.long_td - self.long_td_frozen
            yd_available: int = self.long_yd - self.long_yd_frozen

        # Split close order to close today/yesterday for SHFE/INE exchange
        if req.exchange in {Exchange.SHFE, Exchange.INE}:
            reqs: List[OrderRequest] = []
            volume_left: float = req.volume

            if td_available:
                td_volume: int = min(td_available, volume_left)
                volume_left -= td_volume

                td_req: OrderRequest = copy(req)
                td_req.offset = Offset.CLOSETODAY
                td_req.volume = td_volume
                reqs.append(td_req)

            if volume_left and yd_available:
                yd_volume: int = min(yd_available, volume_left)
                volume_left -= yd_volume

                yd_req: OrderRequest = copy(req)
                yd_req.offset = Offset.CLOSEYESTERDAY
                yd_req.volume = yd_volume
                reqs.append(yd_req)

            if volume_left > 0:
                open_volume: int = volume_left

                open_req: OrderRequest = copy(req)
                open_req.offset = Offset.OPEN
                open_req.volume = open_volume
                reqs.append(open_req)

            return reqs
        # Just use close for other exchanges
        else:
            reqs: List[OrderRequest] = []
            volume_left: float = req.volume

            if pos_available:
                close_volume: int = min(pos_available, volume_left)
                volume_left -= pos_available

                close_req: OrderRequest = copy(req)
                close_req.offset = Offset.CLOSE
                close_req.volume = close_volume
                reqs.append(close_req)

            if volume_left > 0:
                open_volume: int = volume_left

                open_req: OrderRequest = copy(req)
                open_req.offset = Offset.OPEN
                open_req.volume = open_volume
                reqs.append(open_req)

            return reqs
