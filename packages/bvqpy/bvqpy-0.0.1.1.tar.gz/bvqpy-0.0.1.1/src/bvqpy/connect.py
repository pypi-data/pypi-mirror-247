def connect(email, password):
    """
    Connect to formr API 
    """

    r = requests.get('https://formr.org', auth=(email, password))
    if (r.status_code == 200):
        print('Connected to formr')
    else:
        print('Failed to connect: Error ' + r.status_code)
