class Code:
    NOT_ENOUGH_PARAMETERS = 0
    SECRET_KEY_NOT_EXISTS = 1
    OK = 2
    RIG_NEED_REGISTER = 3
    BAD_PARAMETER = 4
    CONNECTION_ALREADY_REGISTERED = 5
    CONNECTION_SAME_SIDE_IDS = 6
    CONNECTION_NOT_FOUND_SIDE_ID = 7


class Protocol:
    PROTO_HOST = 'http://163.172.189.169'
    PROTO_ENDPOINT = PROTO_HOST + '/protocol/'

    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.configuration = []

    def setConfiguration(self, config):
        self.configuration = config

    def getConfiguration(self):
        return self.configuration

    def register_rig(self):
        log('REGISTER', 'Registering rig information...')
        os_name = platform.system()
        payload = urllib.parse.urlencode({
            'key': self.secret_key,
            'os': os_name,
            'mac': get_mac_address(),
            'o_ver': VERSION
        })
        response = self.make_request(self.PROTO_ENDPOINT + 'register?' + payload).json()
        if response['code'] == ProtocolCode.OK:
            # save miner configurations
            log('REGISTER', 'Saving configuration')
            with open('miner.settings', 'w') as f:
                f.write(json.dumps(response['data']))

            self.setConfiguration(response['data'])  # set configuration on possibly reload

            # download miner
            log('REGISTER', 'Downloading miner')
            minerFile = self.make_request(self.PROTO_ENDPOINT + 'miner/' + response['data']['type'])
            with open("miner.zip", "wb") as code:
                code.write(minerFile.content)

            # unzip miner
            zip_ref = zipfile.ZipFile("miner.zip", 'r')
            zip_ref.extractall(".")
            zip_ref.close()

            # delete miner temp
            os.remove('miner.zip')

            log('REGISTER', 'Registration success!')
        else:
            log('ERROR', 'Unknown error on register_rig function')

    def make_request(self, request):
        try:
            req = requests.get(request)
        except requests.exceptions.RequestException as e:
            log('NETWORK', 'Network is unreachable. Waiting a minute...')
            time.sleep(60)
            return self.make_request(request)
        return req

    def make_post_request(self, url, payload):
        try:
            req = requests.post(url, data=payload)
        except requests.exceptions.RequestException as e:
            log('NETWORK', 'Network is unreachable. Waiting a minute...')
            time.sleep(60)
            return self.make_post_request(url, data)
        return req

    def ping(self):
        # prepare miner data payload (temp/speed/name)
        minerPayload = []

        if int(self.configuration['type']) == MinerType.EWBF:
            minerPayload = json.dumps(EWBF.getMinerData())

        payload = {'key': self.secret_key, 'miner': minerPayload}
        response = self.make_post_request(self.PROTO_ENDPOINT + 'ping', payload).json()
        if response['code'] == ProtocolCode.SECRET_KEY_NOT_EXISTS:
            log('SECURITY', 'Wrong security key!')
            sys.exit(-1)
        else:
            if response['code'] == ProtocolCode.RIG_NEED_REGISTER:
                log('SECURITY', 'Configuration changed, going to register')
                return self.register_rig()
            if response['code'] == ProtocolCode.OK:
                log('PING', 'Success')

    def check_connection(self):
        try:
            requests.get(self.PROTO_HOST)
        except requests.exceptions.RequestException as e:
            log('NETWORK', 'No access to protocol host. Network connection is bad?')
            time.sleep(2000)
            sys.exit(-1)