class EWBF:

    @staticmethod
    def getMinerData():
        minerData = requests.get('http://127.0.0.1:25000/getstat').json()
        passed_secs = int(time.time()) - int(minerData['start_time'])
        sendedData = []
        # prevent send zero values on miner start
        if passed_secs > 60:
            for gpu in minerData['result']:
                sendedData.append({
                    'name': gpu['name'],
                    'temp': gpu['temperature'],
                    'speed': gpu['speed_sps']
                })
        return sendedData

    @staticmethod
    def getCmd(configuration):
        cmd = 'miner.exe --server ' + configuration['host'] + ' --port ' + configuration['port'] + ' --user ' + configuration['username'] + ' --api 0.0.0.0:25000'
        if configuration['password'] != '':
            cmd += ' --pass ' + configuration['password']
        return cmd
