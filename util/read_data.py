"""
This code demonstrate how to read data
"""
import sys, os
import os.path as osp
import cv2
import numpy as np
import scipy.io as sio

def write_obj_with_colors(obj_name, vertices, triangles, colors, kpt_ind):
    ''' Save 3D face model with texture represented by colors.
    Args:
        obj_name: str
        vertices: shape = (nver, 3)
        triangles: shape = (ntri, 3)
        colors: shape = (nver, 3)
    '''
    triangles = triangles.copy()
    triangles += 1 # meshlab start with 1

    if obj_name.split('.')[-1] != 'obj':
        obj_name = obj_name + '.obj'
        
    # write obj
    with open(obj_name, 'w') as f:
        # write vertices & colors
        for i in range(vertices.shape[0]):
            s = 'v {} {} {} {} {} {}\n'.format(vertices[i, 0], vertices[i, 1], vertices[i, 2], colors[i, 0], colors[i, 1], colors[i, 2])
            if i in kpt_ind:
                s = 'v {} {} {} 255 0 0\n'.format(vertices[i, 0], vertices[i, 1], vertices[i, 2])
            
            f.write(s)

        # write f: ver ind/ uv ind
        [k, ntri] = triangles.shape
        for i in range(triangles.shape[0]):
            s = 'f {} {} {}\n'.format(triangles[i, 0], triangles[i, 1], triangles[i, 2])
            f.write(s)


def load_mat(data):
    reg_v = data['v'][0][0].astype(np.float32)
    reg_f = data['f'][0][0].astype(int) - 1
    reg_tex = data['tex'][0][0].astype(np.float32)
    reg_kpt_ind = data['kpt_ind'][0][0].astype(int) - 1
    print('vertices shape: ', reg_v.shape)
    print('faces shape: ', reg_f.shape)
    print('texture shape: ', reg_tex.shape)
    print('kpt shape: ', reg_kpt_ind.shape)
    return reg_v, reg_f, reg_tex, reg_kpt_ind


def main():
    gt_info = sio.loadmat('sample/mesh/fusion/gt.mat')   
    # load registration result
    registration = gt_info['neck_obj09']
    reg_v, reg_f, reg_tex, reg_kpt_ind = load_mat(registration)
    # load ground truth in the same way
    gt = gt_info['new_kpt_gt_obj']
    gt_v, gt_f, gt_tex, gt_kpt_ind = load_mat(gt)
      
    # save as obj
    res_dir = "objs"
    if not osp.exists(res_dir):
        os.mkdir("objs")
    write_obj_with_colors('objs/reg.obj', reg_v, reg_f, reg_tex, reg_kpt_ind)
    write_obj_with_colors('objs/gt.obj', gt_v, gt_f, gt_tex, gt_kpt_ind)

    
if __name__ == '__main__':
    main()
