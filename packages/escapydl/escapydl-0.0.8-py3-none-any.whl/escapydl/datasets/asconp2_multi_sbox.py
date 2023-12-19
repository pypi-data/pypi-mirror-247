import os
import torch
import Utils
import numpy as np
import helpers.ascon_helper as ascon

parameters = {
    "dataset_name"        : "data/ASCON_P2_CPA_all_mlpsca_ready.trs",
    "dataset_size"        : 510000,
    "training_size"       : 50000,
    "val_size"            : 5000,
    "subkey"              : [x for x in range(64)],
    "num_key_hypotheses"  : 4,
    "n_samples"           : 1408,
    "r"                   : 0.6,
    "n_repeat"            : 50,
    "ge_rate"             : 5,
    "shuffle"             : True,
}

model = {
    "num_epochs"          : 200,
    "loss_function"       : Utils.FocalLoss(),
    "lr"                  : 1e-03,
    "bs"                  : 512,
    "activation_function": "relu", 
    "pooling": "average",
    "optimizer": "radam",
    "weight_init": "he_uniform",
    "n_conv_block": 2,
    "kernel_size_0": 30, 
    "c_out_0": 8,
    "kernel_size_1": 5,
    "c_out_1": 16, 
#    "kernel_size_2": 6,
#    "c_out_2": 32, 
    "lr": 1e-3,  
    "n_layers": 4, 
    "n_units_l0": 500, 
    "n_units_l1": 470,
    "n_units_l2": 10,
    "n_units_l3": 480,
#    "n_units_l4": 100,
#    "n_units_l5": 100,
#    "n_units_l6": 100,
#    "n_units_l7": 100,
                           
}

callbacks = {
    "modelcheckpoint":{
        "period":-1,
    },
    "guessingentropy":{
        "ge_rate":5,
        "n_repeat":50,
        "r":0.6,
    },
    "tensorboard":{
        "training_accuracy":True,
        "validation_accuracy":True,
        "training_loss":True,
        "validation_loss":True,
    },
}

def get_attack_parameters(traceset, subkey, index):
    """Returns a dictionary of parameters to be used to search for attack .
    To be used before calling intermediate_value().

    :param traceset: Traceset to use
    :type traceset: dict
    :param subkey: Subkey to attack
    :type subkey: int
    :param index: Index of the traceset to use
    :type index: int or slice
    :return: Dictionary of parameters
    :rtype: dict
    """        
    return {'nonce0':traceset["nonce0"][index],
            'nonce1':traceset["nonce1"][index],
            'subkey':subkey}

def get_known_key(traceset, subkey, index):
    return ascon.select_subkey_sbox(subkey, traceset['key'][index])

def intermediate_value(keyguess, trace_parameters):
    """Return the intermediate value of a key in the SBox . 
    nonce0 and nonce1 should be byte arrays of size (8) as they both are half of the nonce length (16 bytes).
    k should be a 3-bit value as an integer. This bit corresponds to the part of the key concerned in the attack given subkey.

    :param trace_parameters: Dictionary containing the trace parameters for intermediate value computation
    :type trace_parameters: dict
    :return: Intermediate value
    :rtype: Any
    """        
    return ascon.intermediate_value_sbox(keyguess,trace_parameters)