from app import celery

import time

@celery.task(bind=True)
def predict(self, filename):
    # Open image
    
    # TODO: predict if it's a cat or a dog
    self.update_state(state='PROGRESS', meta={'status': 'Running'})
    time.sleep(5)
    self.update_state(state='PROGRESS', meta={'status': 'Running 2'})
    time.sleep(5)
    self.update_state(state='PROGRESS', meta={'status': 'Running 3'})
    time.sleep(5)
    self.update_state(state='PROGRESS', meta={'status': 'Running 4'})
    time.sleep(5)
    return {'status': 'Completed', 'result': filename}
