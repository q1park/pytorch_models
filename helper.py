import matplotlib.pyplot as plt
import numpy as np
from torch import nn, optim
from torch.autograd import Variable

def view_probability(model, test_set, test_ind, version):
    model.eval()

    images, labels = iter(torch.utils.data.DataLoader(test_set[test_ind], batch_size=1) )

    img = images.view(images.shape[0], -1)
    img = img
    
    with torch.no_grad():
        pshape = torch.exp(model.forward(img) );

    return helper.view_classify(images[0], pshape, version = version);

def make_checkpoint(model, check_name):
    checkpoint = {'input_size': model.hidden_layers[0].in_features,
                  'output_size': model.output.out_features,
                  'hidden_layers': [each.out_features for each in model.hidden_layers],
                  'state_dict': model.state_dict()}

    
    torch.save(checkpoint, check_name)

def load_checkpoint(filepath):
    checkpoint = torch.load(filepath)
    model = Network(checkpoint['input_size'],
                             checkpoint['output_size'],
                             checkpoint['hidden_layers'])
    model.load_state_dict(checkpoint['state_dict'])
    
    return model

def test_network(net, trainloader):

    criterion = nn.MSELoss()
    optimizer = optim.Adam(net.parameters(), lr=0.001)

    dataiter = iter(trainloader)
    images, labels = dataiter.next()

    # Create Variables for the inputs and targets
    inputs = Variable(images)
    targets = Variable(images)

    # Clear the gradients from all Variables
    optimizer.zero_grad()

    # Forward pass, then backward pass, then update weights
    output = net.forward(inputs)
    loss = criterion(output, targets)
    loss.backward()
    optimizer.step()

    return True


def imshow(image, ax=None, title=None, normalize=True):
    """Imshow for Tensor."""
    if ax is None:
        fig, ax = plt.subplots()
    image = image.numpy().transpose((1, 2, 0))

    if normalize:
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        image = std * image + mean
        image = np.clip(image, 0, 1)

    ax.imshow(image)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', length=0)
    ax.set_xticklabels('')
    ax.set_yticklabels('')

    return ax


def view_recon(img, recon):
    ''' Function for displaying an image (as a PyTorch Tensor) and its
        reconstruction also a PyTorch Tensor
    '''

    fig, axes = plt.subplots(ncols=2, sharex=True, sharey=True)
    axes[0].imshow(img.numpy().squeeze())
    axes[1].imshow(recon.data.numpy().squeeze())
    for ax in axes:
        ax.axis('off')
        ax.set_adjustable('box-forced')

def view_classify(img, ps, version="CatDog"):
    ''' Function for viewing an image and it's predicted classes.
    '''
    ps = ps.data.numpy().squeeze()

    fig, (ax1, ax2) = plt.subplots(figsize=(6,9), ncols=2)
    ax1.imshow(img.numpy().transpose((1, 2, 0)).squeeze())
    ax1.axis('off')
    
    if version == "MNIST":
        ax2.set_yticklabels(np.arange(10))
        ax2.barh(np.arange(10), ps)
        ax2.set_aspect(0.1)
        ax2.set_yticks(np.arange(10))
    elif version == "Fashion":
        ax2.set_yticklabels(['T-shirt/top',
                            'Trouser',
                            'Pullover',
                            'Dress',
                            'Coat',
                            'Sandal',
                            'Shirt',
                            'Sneaker',
                            'Bag',
                            'Ankle Boot'], size='small');
        ax2.barh(np.arange(10), ps)
        ax2.set_aspect(0.1)
        ax2.set_yticks(np.arange(10))
    elif version == "CatDog":
        ax2.set_yticklabels(['Cat',
                             'Dog'], size='small');
        ax2.barh(np.arange(2), ps)
        ax2.set_aspect(0.1)
        ax2.set_yticks(np.arange(2))
    ax2.set_title('Class Probability')
    ax2.set_xlim(0, 1.1)

    plt.tight_layout()
