from odoo import fields, models
from datetime import datetime, timedelta


import requests

class ErAuction(models.Model):

    _name = "er.auction"
    _order = 'sequence'
    _description = 'Auction'


    name = fields.Char(string='ID')
    sender = fields.Char(string='Sender')
    code = fields.Char(string='Code')
    instrument = fields.Char(string='Instrument')
    status = fields.Char(string='Status')
    is_public = fields.Boolean(string='Is Public')
    direction = fields.Char(string='Direction')
    ccp_account = fields.Char(string='CCP Account')
    type = fields.Char(string='Type')
    currency = fields.Char(string='Currency')
    volume = fields.Float(string='Volume')
    lot_size = fields.Float(string='Lot Size')
    announce_time = fields.Char(string='Announce Time')
    start_time = fields.Char(string='Start Time')
    close_time = fields.Char(string='Close Time')
    settlement_start_date = fields.Char(string='Settlement Start Date')
    settlement_end_date = fields.Char(string='Settlement End Date')
    min_price = fields.Float(string='Min Price')
    max_price = fields.Float(string='Max Price')
    time = fields.Char(string='Time')
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

    def _get_auction_info(self):
        session = self.login_to_external_system('admin01', 'a')

        # Get contract info using the same session object
        auction_url = 'http://demo.erdenesit.mn:8070/ts/auction/list'
        response = session.get(auction_url)

        auction_url = 'http://demo.erdenesit.mn:8070/ts/auction/list'
        response = session.get(auction_url)

        if response.status_code == 200:
            data = response.json()
            for auction in data:
                auctionObj = self.env['er.auction'].search(
                    [('name', '=', auction['id'])], limit=1)
                if not auctionObj:
                    er_auction_vals = {
                        'name': auction['id'],
                        'sender': auction['sender'],
                        'code': auction['code'],
                        'instrument': auction['instrument'],
                        'status': auction['status'],
                        'is_public': auction['isPublic'],
                        'direction': auction['direction'],
                        'ccp_account': auction['ccpAccount'],
                        'type': auction['type'],
                        'currency': auction['currency'],
                        'volume': auction['volume'],
                        'lot_size': auction['lotSize'],
                        'announce_time': auction['announceTime'],
                        'start_time': self.convert_timestamp(auction['startTime']),
                        'close_time': self.convert_timestamp(auction['closeTime']),
                        'settlement_start_date': self.convert_timestamp(auction['settlementStartDate']),
                        'settlement_end_date': self.convert_timestamp('settlementEndDate'),
                        'min_price': auction['minPrice'],
                        'max_price': auction['maxPrice'],
                        'time': auction['time'],
                    }
                    self.env['er.auction'].sudo().create(er_auction_vals)

    def convert_timestamp(self, timestamp):
        try:
            input_formats = ['%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%f%z']
            output_format = '%Y-%m-%d %H:%M:%S'
            added_hours = 5

            dt = None

            # Try different input formats until a match is found
            for format_str in input_formats:
                try:
                    dt = datetime.strptime(timestamp, format_str)
                    break
                except ValueError:
                    pass

            if dt is None:
                raise ValueError("Invalid timestamp format")

            # Add specified hours to the datetime object
            dt += timedelta(hours=added_hours)

            # Convert the datetime object to the desired output format
            formatted_timestamp = dt.strftime(output_format)

            return formatted_timestamp
        except:
            return False

