#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:27:27 2017

@author: jeremy
"""

from matplotlib import use

from pylab import *
from scipy.stats import beta, norm, uniform
from random import random
from numpy import *
import numpy as np
import os
import seaborn as sns



#Don't edit anything past here
#function to graph posteriors and joint posteriors
def graph(N,s,prior_params,pdf_arr):
    fig, (ax,bx) = plt.subplots(2, 1)
    x = np.linspace(0,1,1000)
    ax.plot(x, beta.pdf(x,prior_params[0][0] + s[0] - 1,prior_params[0][1] + N[0] - s[0] - 1),                        'r-', lw=5, alpha=0.6, label='beta pdf')
    ax.set_title('Posterior A density')
    ax.axis([0,0.1,0,max(beta.pdf(x,prior_params[0][0] + s[0] - 1,prior_params[0][1] + N[0] - s[0] - 1))+10])
    bx.plot(x, beta.pdf(x,prior_params[1][0] + s[1] - 1,prior_params[1][1] + N[1] - s[1] - 1),                        'r-', lw=5, alpha=0.6, label='beta pdf')
    bx.set_title('Posterior B density')
    bx.axis([0,0.1,0,max(beta.pdf(x,prior_params[1][0] + s[1] - 1,prior_params[1][1] + N[1] - s[1] - 1))+10])
    xticks=np.linspace(0,1.02,103)
    fig2, (cx) = plt.subplots(1, 1)
    cx = sns.heatmap(pdf_arr,xticklabels=10,yticklabels=10,cmap="Spectral_r")
    cx.set_xticklabels(xticks)
    cx.set_yticklabels(xticks[::-1])
    cx.set_xlabel('Posterior A density')
    cx.set_ylabel('Posterior B density')
    cx.set_title('Joint Posterior density')
    cx.invert_yaxis()
    cx.plot([0,1024],[1024,0],'k-',lw=1)
    cx.axis([0,100,1024,924])
    return 0

def bayesian_test(N,s,prior_params,threshold_of_caring):
    degrees_of_freedom = len(prior_params)
    posteriors = []
    for i in range(degrees_of_freedom):
        posteriors.append( beta(prior_params[i][0] + s[i] - 1, prior_params[i][1] + N[i] - s[i] - 1) )

    if degrees_of_freedom == 2:
        xgrid_size = 1024

        x = mgrid[0:xgrid_size,0:xgrid_size] / float(xgrid_size)
        # Compute joint posterior, which is a product distribution
        pdf_arr = posteriors[0].pdf(x[1]) * posteriors[1].pdf(x[0])
        pdf_arr /= pdf_arr.sum() # normalization

        prob_error = zeros(shape=x[0].shape)
        if (s[1] / float(N[1])) > (s[0] / float(N[0])):
            prob_error[where(x[1] > x[0])] = 1.0
        else:
            prob_error[where(x[0] > x[1])] = 1.0
                                    
        expected_error = maximum(abs(x[0]-x[1]),0.0)

        expected_err_scalar = (expected_error * prob_error * pdf_arr).sum()
    
        if (expected_err_scalar < threshold_of_caring):
            if (s[1] / float(N[1])) > (s[0] / float(N[0])):
                print("Probability that version B is larger is " + str(1-(prob_error*pdf_arr).sum()))
                print("Terminate test. Choose version B. Expected error is " + str(expected_err_scalar))
                #graph(N,s,prior_params,pdf_arr)
            else:
                print("Probability that version A is larger is " + str(1-(prob_error*pdf_arr).sum()))
                print("Terminate test. Choose version A. Expected error is " + str(expected_err_scalar))
                #graph(N,s,prior_params,pdf_arr)
        else:
            print("Probability that version B is larger is " + str(1-(prob_error*pdf_arr).sum()))
            print("Continue test. Expected error was " + str(expected_err_scalar) + " > " + str(threshold_of_caring))
            
        return expected_err_scalar,pdf_arr