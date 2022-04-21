import threading
import time


class DataManager:
    def __init__(self, connection_manager, data_processor):
        self._updatePeriod = 10
        self._connectionManager = connection_manager
        self._dataProcessor = data_processor
        self._running = True
        self._thread = threading.Thread(target=self.update)

    def update(self):
        while self._running:
            for cw in self._connectionManager.conWrap:
                self._dataProcessor.process(cw.get_licence_plate(), cw.update(self._updatePeriod))
            time.sleep(self._updatePeriod)



