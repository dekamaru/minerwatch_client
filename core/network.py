def make_request(url):
    try:
        requests.get(self.PROTO_HOST)
    except requests.exceptions.RequestException as e:
        log('NETWORK', 'No access to protocol host. Network connection is bad?')
        time.sleep(2000)
        sys.exit(-1)

