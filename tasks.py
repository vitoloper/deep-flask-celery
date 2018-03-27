from fastai.imports import *
from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *
from fastai.dataset import *
from fastai.sgdr import *
from fastai.plots import *
from fastai.sgdr import *
from fastai.plots import *

from app import celery

# fast.ai configuration
sz=224

# Disable CUDA
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Load the model, load data and create a learner
model = torch.load(celery.conf['torch_model'], map_location=lambda storage, location: storage)
data = ImageClassifierData.from_paths(celery.conf['data_folder'], tfms=tfms_from_model(model, sz))
learn = Learner.from_model_data(model, data)

@celery.task(bind=True)
def predict(self, filename):
    self.update_state(state='PROGRESS', meta={'status':'Predicting'})
    
    # We don't care about trn_tfms, hence the _
    _, val_tfms = tfms_from_model(model, sz)
    im = val_tfms(open_image(filename))
    
    # Use the CPU for prediction
    # T(x): make a tensor
    # V(x): make a Variable (A PyTorch Variable is a wrapper around a PyTorch Tensor, and represents a node in a computational graph.)
    # http://pytorch.org/tutorials/beginner/pytorch_with_examples.html#pytorch-variables-and-autograd
    learn.model.eval()
    preds = to_np(learn.model(V(T(im[None]))))
    np.exp(preds)

    print(np.argmax(preds))     # 0: cat, 1: dog 
    print(np.exp(preds))

    result = 'unknown'
    if np.argmax(preds) == 1:
        result = 'dog'
    elif np.argmax(preds) == 0:
        result = 'cat'

    listprob = np.exp(preds).tolist()

    return {'status': 'Completed', 'result': result, 'cat_prob': listprob[0][0], 'dog_prob': listprob[0][1]}
