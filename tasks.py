from app import celery

import time

@celery.task(bind=True)
def predict(self, x, y):
    # TODO: long calculations here
    self.update_state('PROGRESS')
    time.sleep(10)
    result = x + y
    return {'status': 'Completed', 'result': result}
