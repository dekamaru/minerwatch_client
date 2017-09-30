def observer_thread(proto):
    log('OBSERVER', 'Thread started')
    while True:
        proto.ping()
        time.sleep(300)