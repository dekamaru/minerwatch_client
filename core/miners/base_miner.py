class BaseMiner:

    """
    Should return data list
    [
        [
            'name' => 'GPU NAME',
            'temp' => 'GPU TEMP',
            'speed' => 'GPU SPEED'
        ]
    ]
    """
    def get_data(self): pass

    """
    Should return run command line for implemented miner
    :arg configuration Account configuration
    """
    def get_command(self, configuration): pass