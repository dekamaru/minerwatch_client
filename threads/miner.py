def miner_thread(configuration, proto):

    if int(configuration['type']) == MinerType.EWBF:
        cmd = EWBF.getCmd(configuration)

    log('MINER', 'Starting miner: ' + cmd)
    while True:
        p = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        p.wait()
        log('MINER', 'Miner was crashed. Restart...')