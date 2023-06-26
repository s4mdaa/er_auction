from datetime import datetime, timedelta
from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
import json


class CustomAuthSignupHome(AuthSignupHome):
    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kwargs):
        response = super(CustomAuthSignupHome, self).web_login(
            redirect=redirect, **kwargs)
        if not request.session.uid:
            return response
        else:
            if request.env.user.login != 'ssamdaa119@gmail.com':
                return request.redirect('/auctions')
            else:
                return request.redirect('/web')

    @http.route('/auctions', type='http', auth='user', website=True, sitemap=False)
    def auctions(self):
        auctions = request.env['er.auction'].search([])
        values = {
            'auctions': auctions,
        }
        return request.render('er_auction.auctions_page', values)
    
    @http.route('/auction/<model("er.autcion"):auction>', type='http', auth='user', website=True, sitemap=False)
    def auction(self, auction):
        accounts = self.get_porfolio_accounts()
        values = {
            'auction': auction,
            'accounts': accounts,
        }
        return request.render('er_auction.auction_page', values)
    

    @http.route(
        ['/auction/place/bid'],
        type='http', auth="user", website=True)
    def auction_place_bid(self, **post):
        auction_obj = request.env['er.auction'].sudo().search([('code','=', post.get('auctionId'))])
        
        auction_order_obj = request.env['er.auction.order'].search([], limit=1)

        participant = self.get_participant()

        portfolio = self.get_portfolio()

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        formatted_datetime = formatted_datetime + '+00:00'

        auction_order_values = {
            'quantity': float(post.get('volume')),
            'price': float(post.get('price')),
            'account': post.get('account'),
            'instrument': auction_obj.code,
            'auction': auction_obj.code,
            'currency': auction_obj.currency,
            'date': formatted_datetime,
            'lastModifiedDate': formatted_datetime,
            'participant': participant,
            'portfolio': portfolio,
        }

        auction_order_obj._create_auction_order(auction_order_values)
    
        return request.redirect('/auctions')
        
    def get_participant(self):
        auction_obj = request.env['er.auction'].search([], limit=1)
        username = request.env.user.login
        session = auction_obj.login_to_external_system(username, '1')

        # Get contract info using the same session object
        user_url = 'http://demo.erdenesit.mn:8070/user/list'
        response = session.get(user_url)

        user_url = 'http://demo.erdenesit.mn:8070/user/list'
        response = session.get(user_url)

        if response.status_code == 200:
            user = response.json()
            return user[0]['participant']
        

    def get_portfolio(self):
        auction_obj = request.env['er.auction'].search([], limit=1)
        username = request.env.user.login
        session = auction_obj.login_to_external_system(username, '1')

        # Get contract info using the same session object
        portfolio_url = 'http://demo.erdenesit.mn:8070/ts/portfolio/list'
        response = session.get(portfolio_url)

        portfolio_url = 'http://demo.erdenesit.mn:8070/ts/portfolio/list'
        response = session.get(portfolio_url)

        if response.status_code == 200:
            portfolio = response.json()
            return portfolio[0]['code']
        

    @http.route('/auction_orders', type='http', auth='user', website=True, sitemap=False)
    def auction_orders(self, **kw):
        ordersObj = request.env['er.auction.order'].search([('auction', '=', kw.get('auctionCode'))])
        auction = request.env['er.auction'].search([('code', '=', kw.get('auctionCode'))])
        if request.env.user.login == 'TraderA1':
            accountCode = 'A01'
        elif request.env.user.login == 'TraderB1':
            accountCode = 'B01'
        else:
            accountCode = 'C01'
        
        accountsObj = request.env['er.portfolio.account'].search([('code', 'like', accountCode)])
        orders = []
        for orderObj in ordersObj:

            order = {
                'date': auction.convert_timestamp(orderObj.date),
                'account': orderObj.account,
                'price': orderObj.price,
                'volume': orderObj.quantity,
            }
            orders.append(order)

        accounts = []
        for accountObj in accountsObj:
            account = {
                'name': accountObj.name,
                'code': accountObj.code,
            }
            accounts.append(account)

        data = {
            'orders': orders,
            'auctionCode': auction.code,
            'auctionCloseTime': auction.close_time,
            'auctionName': auction.name,
            'accounts': accounts,
        }
        return json.dumps(data)
        