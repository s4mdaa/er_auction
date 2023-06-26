from odoo import fields, models

class ErPortfolioAccount(models.Model):

    _name = "er.portfolio.account"
    _order = 'sequence'
    _description = 'Portfolio Account'

    name = fields.Char(string='ID')
    code = fields.Char(string='Code')
    sequence = fields.Integer(
        string='Sequence',
        default=100,
        copy=False
    )


    def get_porfolio_accounts(self):
        auction_obj = self.env['er.auction'].search([], limit=1)
        session = auction_obj.login_to_external_system('admin01', 'a')

        # Get contract info using the same session object
        portfolio_account_url = 'http://demo.erdenesit.mn:8070/ts/portfolio/account/list'
        response = session.get(portfolio_account_url)

        portfolio_account_url = 'http://demo.erdenesit.mn:8070/ts/portfolio/account/list'
        response = session.get(portfolio_account_url)

        if response.status_code == 200:
            data = response.json()
            for account in data:
                accountObj = self.env['er.portfolio.account'].search(
                    [('code', '=', account['code'])], limit=1)
                if not accountObj:
                    er_account_vals = {
                        'name': account['name'],
                        'code': account['code'],
                    }
                    self.env['er.portfolio.account'].sudo().create(er_account_vals)


