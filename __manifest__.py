{
    # Theme information

    'name': 'Energy Resource Auction',
    'category': 'Operations',
    'version': '1.0.0',
    'license': 'OPL-1',
    'depends': ['web', 'portal'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/demo_data.xml',

        'templates/auctions_page.xml',

        'views/menu_view.xml',
        'views/auction_view.xml',
        'views/auction_order_view.xml',



    ],

    'assets': {
        'web.assets_frontend': [
            "/er_auction/static/**/*",
        ]
    },

    # Author
    'author': 'Energy Resource',
    'maintainer': 'Samdaa',

    # Technical
    'installable': True,
    'auto_install': False,
}
