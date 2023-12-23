import numpy as np
from sklearn.decomposition import PCA

def unravel(c, n_steps=3):
    Z = [np.zeros_like(c), c]    
    for i in range(n_steps):
        z = Z[-1]*Z[-1] + c
        Z.append(z)
    return np.array(Z)

def images_to_rgb(images, overscale=0):
    history = images.shape[0]
        
    pca = PCA(n_components=3+overscale)
    
    flatten_image = images.reshape(history, -1).T
    flatten_image[np.isnan(flatten_image)] = 0
    
    transformed_image = pca.fit_transform(flatten_image)
    
    rgb = transformed_image.reshape(*images.shape[1:], 3 + overscale)[:,:,:3]
    return pca, rgb


def hexpose(events, margin=1, resolution=32, translation=[0,0]):    
    print(events.shape)
    n_paths, n_objects = events.shape

    # Open events
    images = []
    for path_id in range(n_paths):
        pevents = events[path_id]

        events_open = np.array([pevents.real, pevents.imag]).T
        
        _margin = np.array([margin, margin]) - np.array(translation)
    
        # Identify nans
        is_not_nan = np.sum(np.isnan(events_open), axis=1) == 0
        
        # Identify margins
        is_larger = np.sum(events_open > _margin, axis=1) > 0
        is_smaller = np.sum(events_open < -_margin, axis=1) > 0

        # Create mask
        is_present = is_not_nan * (~is_larger * ~is_smaller)

        # Establish present events
        present_events = events_open[is_present]
        present_events = present_events[np.sum(present_events, axis=1)!=0]
            
        # Quantize events
        q_events = np.rint((resolution-1)*(present_events+margin)/(2*margin))
        q_events = q_events.astype(np.int64)
        
        # Prepare image
        image = np.ones((resolution, resolution))
        
        for event in q_events:
            image[event[0], event[1]] += 1
        
        image /= np.max(image)
        images.append(image)
        
    images = np.array(images)
    print(images.shape)
        
    return images

def expose(events, margin=1, resolution=32, translation=[0,0]):    
    # Open events
    raveled_events = events.ravel()
    events_open = np.array([raveled_events.real, raveled_events.imag]).T
    
    _margin = np.array([margin, margin]) - np.array(translation)
    
    # Identify nans
    is_not_nan = np.sum(np.isnan(events_open), axis=1) == 0
    
    # Identify margins
    is_larger = np.sum(events_open > _margin, axis=1) > 0
    is_smaller = np.sum(events_open < -_margin, axis=1) > 0

    # Create mask
    is_present = is_not_nan * (~is_larger * ~is_smaller)

    # Establish present events
    present_events = events_open[is_present]
    present_events = present_events[np.sum(present_events, axis=1)!=0]
        
    # Quantize events
    q_events = np.rint((resolution-1)*(present_events+margin)/(2*margin))
    q_events = q_events.astype(np.int64)
    
    # Prepare image
    image = np.ones((resolution, resolution))
    
    for event in q_events:
        image[event[0], event[1]] += 1
    
    image /= np.max(image)
    
    return image