#Effiliation API Client

Client for the Effiliation API http://apiv2.effiliation.com/apiv2/doc/home.htm

## Install

From source

    python setup.py build
    sudo python setup.py install

## Quickstart

Fetch your programs

    from effiliation.client import Client
    cli = Client('MY API KEY')
    print cli.get_programs()

Fetch vouchers

    from effiliation.client import Client
    cli = Client('MY API KEY')
    print cli.get_promotional_offers({'type': 'bp'})
