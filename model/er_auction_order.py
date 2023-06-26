from odoo import api, fields, models
import uuid
import requests


class ErAuctionOrder(models.Model):

    _name = "er.auction.order"
    _order = 'sequence'
    _description = 'Auction Order'

    name = fields.Char(string='ID')
    sender = fields.Char()
    reference = fields.Char()
    auction = fields.Char()
    state = fields.Char()
    type = fields.Char()
    direction = fields.Char()
    flag = fields.Char()
    instrument = fields.Char()
    price = fields.Float()
    price_type = fields.Char()
    yield_amount = fields.Float()
    quantity = fields.Float()
    date = fields.Char()
    delivery_point = fields.Char()
    account = fields.Char()
    currency = fields.Char()
    sequence = fields.Integer(
        string='Sequence',
        default=100,
        copy=False
    )

    def login_to_external_system(self, username, password):
        session = requests.Session()

        # Login
        login_url = 'http://demo.erdenesit.mn:9000/login'
        payload = {
            'username': username,
            'password': password,
        }
        response = session.post(login_url, data=payload)

        if response.status_code == 200:
            # Successful login
            return session
        else:
            # Failed to login
            return None

    def _get_auction_order_info(self):
        session = self.login_to_external_system('admin01', 'a')

        # Get contract info using the same session object
        trade_url = 'http://demo.erdenesit.mn:8070/ts/order/list'
        response = session.get(trade_url)

        trade_url = 'http://demo.erdenesit.mn:8070/ts/order/list'
        response = session.get(trade_url)

        if response.status_code == 200:
            data = response.json()
            for auctionOrder in data: 
                auctionOrderObj = self.env['er.auction.order'].search(
                    [('name', '=', auctionOrder['id'])], limit=1)
                if not auctionOrderObj:
                    er_auction_order_vals = {
                        'name': auctionOrder['id'],
                        'sender': auctionOrder['sender'],
                        'reference': auctionOrder['reference'],
                        'auction': auctionOrder['auction'],
                        'state': auctionOrder['state'],
                        'type': auctionOrder['type'],
                        'direction': auctionOrder['direction'],
                        'flag': auctionOrder['flag'],
                        'instrument': auctionOrder['instrument'],
                        'price': auctionOrder['price'],
                        'price_type': auctionOrder['priceType'],
                        'yield_amount': auctionOrder['yield'],
                        'quantity': auctionOrder['quantity'],
                        'date': auctionOrder['date'],
                        'delivery_point': auctionOrder['deliveryPoint'],
                        'account': auctionOrder['account'],
                        'currency': auctionOrder['currency'],
                    }
                    self.env['er.auction.order'].sudo().create(
                            er_auction_order_vals)
                        

    def _create_auction_order(self, order_values):
        username = self.env.user.login
        generated_uuid = str(uuid.uuid4())
        
        if username == 'TraderA1':
            direction = 'sell'
        else:
            direction = 'buy'
        session = self.login_to_external_system(username, '1')
        create_order_url = 'http://demo.erdenesit.mn:8070/ts/auction/order/new'
        order_payload = {
            "id": generated_uuid,
            "sender": username,
            "partic": order_values['participant'],
            "activity": "executed",
            "auction": order_values['auction'],
            "type": "exchange",
            "direction": direction,
            "instrument": order_values['instrument'],
            "currency": order_values['currency'],
            "quantity": order_values['quantity'],
            "price": order_values['price'],
            "priceType": "actual",
            "flag": "partial",
            "deliveryPoint": "",
            "portfolio": order_values['portfolio'],
            "account": order_values['account'],
            "date": order_values['date'],
            "version": 0,
            "time": 0,
            "lastModifiedDate": order_values['lastModifiedDate']
        }
        response = session.put(create_order_url, json=order_payload)


        create_order_url = 'http://demo.erdenesit.mn:8070/ts/auction/order/new'
        order_payload = {
            "id": generated_uuid,
            "sender": username,
            "partic": order_values['participant'],
            "activity": "executed",
            "auction": order_values['auction'],
            "type": "exchange",
            "direction": direction,
            "instrument": order_values['instrument'],
            "currency": order_values['currency'],
            "quantity": order_values['quantity'],
            "price": order_values['price'],
            "priceType": "actual",
            "flag": "partial",
            "deliveryPoint": "",
            "portfolio": order_values['portfolio'],
            "account": order_values['account'],
            "date": order_values['date'],
            "version": 0,
            "time": 0,
            "lastModifiedDate": order_values['lastModifiedDate']
        }
        response = session.put(create_order_url, json=order_payload)

        # Check create order response status code
        if response.status_code == 200:
            print("Auction order created successfully.")
            self._get_auction_order_info()
        else:
            # Failed to create order
            print("Failed to create auction order.")

