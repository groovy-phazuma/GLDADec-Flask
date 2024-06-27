#!/usr/bin/env python3
"""
Created on 2024-06-24 (Mon) 00:45:58

Conduct Guided LDA deconvolution

@author: I.Azuma
"""
# %%
import pandas as pd

from pathlib import Path
BASE_DIR = Path(__file__).parent.parent.parent  # github repository

import sys
sys.path.append(str(BASE_DIR/'GLDADec'))
from run import pipeline


def run_simple_gldadec():
    raw_df = pd.read_csv(BASE_DIR/'GLDADec'/'data'/'GSE237801'/'mouse_dili_expression.csv',index_col=0)
    marker_dic = pd.read_pickle(BASE_DIR/'GLDADec'/'data'/'marker'/'mouse_liver_CellMarker.pkl')
    random_sets = pd.read_pickle(BASE_DIR/'GLDADec'/'data'/'random_info'/'100_random_sets.pkl')

    # single run and evaluation
    pp = pipeline.Pipeline(verbose=False)
    pp.from_predata(raw_df,target_samples=['Ctrl', 'APAP'],
                    do_ann=False,linear2log=False,log2linear=False,
                    do_drop=True,do_batch_norm=False,do_quantile=False)
    pp.gene_selection(method='CV',outlier=True,topn=1000)
    pp.add_marker_genes(target_cells=[],add_dic=marker_dic)
    pp.deconv_prep(random_sets=random_sets,do_plot=False,specific=True,
                   prior_norm=True,norm_scale=1,minmax=True,mm_scale=10)
    pp.deconv(n=10,add_topic=10,n_iter=100,alpha=0.01,eta=0.01,refresh=10,
              initial_conf=1.0,seed_conf=1.0,other_conf=0.0,ll_plot=False,var_plot=False)

    # collect output
    deconv_res = pp.merge_total_res
    deconv_mean = sum(deconv_res)/len(deconv_res)
    fxn = lambda x : round(x,3)
    deconv_mean = deconv_mean.applymap(fxn)

    return deconv_mean

