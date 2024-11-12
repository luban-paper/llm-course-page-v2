import PIL
import os
import shutil
import PIL.Image
import numpy as np
import copy

src_dir = "./pp"
dst_dir = "./pp_new"

if os.path.exists(dst_dir):
    shutil.rmtree(dst_dir)
os.makedirs(dst_dir, exist_ok=True)


def comp_(alpha):
    H, W = alpha.shape
    h_start, h_end = 0, H 
    w_start, w_end = 0, W 
    
    prev_sum = 0
    for h in range(H):
        if prev_sum == 0 and np.sum(alpha[h, :]) > 0:
            h_start = h
        elif prev_sum > 0 and np.sum(alpha[h, :]) == 0:
            h_end = h
        prev_sum = np.sum(alpha[h, :])
    
    prev_sum = 0
    for w in range(W):
        if prev_sum == 0 and np.sum(alpha[:, w]) > 0:
            w_start = w
        elif prev_sum > 0 and np.sum(alpha[:, w]) == 0:
            w_end = w
        prev_sum = np.sum(alpha[:, w])
    
    return h_start, h_end, w_start, w_end
            
            

def main():
    file_list = [i for i in os.listdir(src_dir) if i != ".DS_Store"]
    for fn in file_list:
        img = PIL.Image.open(os.path.join(src_dir, fn)).convert("RGBA")
        img_array = np.array(img)
        alpha = copy.deepcopy(img_array[:, :, 3])
        # crop by alpha
        alpha[alpha > 0] = 1
        alpha = alpha.astype(np.float32)
        print(fn)
        crop_ = comp_(alpha)
        new_img = PIL.Image.fromarray(img_array[crop_[0]: crop_[1], crop_[2]: crop_[3], :], "RGBA")
        new_img.save(os.path.join(dst_dir, fn))
        

if __name__ == "__main__":
    main()