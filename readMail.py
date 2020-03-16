def readmail(volume):
    time.sleep(1.5)
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user, pwd)
    m.select('"[Gmail]/All Mail"')
    resp, items = m.search(None,
                           "NOT SEEN FROM tradingview")
    items = items[0].split()
    for emailid in items:
        resp, data = m.fetch(emailid,
                             "(RFC822)")
        email_body = data[0][1]
        mail = email.message_from_bytes(email_body)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            pair = mail['Subject'].split()[2]
            if mail['Subject'].split()[3] == "Buy":
                m.store(emailid, '+FLAGS', '\Seen')
                print(st + ' \x1b[6;30;42m' + 'Buy' + '\x1b[0m' + ' Triggered on ' + pair)
                logging.info(st + ' Buy' + ' Triggered on ' + pair)
                trade('0', volume, pair)
            if mail['Subject'].split()[3] == "Sell":
                m.store(emailid, '+FLAGS', '\Seen')
                print(st + ' \x1b[6;30;41m' + 'Sell' + '\x1b[0m' + ' Triggered on ' + pair)
                logging.info(st + ' Sell' + ' Triggered on ' + pair)
                trade("1", volume, pair)
        except Exception as e:
            print(e)
            logging.info(e)