import os
import torch
import helpers.xoodyak_helper as xoodyak

parameters = {
    "dataset_name"        : 'data/XOODYAK_HW_50000_NN_attack_20231016_113724_fixed_key.trs',
    "dataset_size"        : 50000,
    "training_size"       : 40000,
    "val_size"            : 10000,
    "subkey"              : 0,
    "num_key_hypotheses"  : 16,
    "n_samples"           : 400,
    "shuffle"             : True,
}

model = {
    "loss_function"       : torch.nn.CrossEntropyLoss(),
    "lr"                  : 1e-03,
    "bs"                  : 128,
    "num_epochs"          : 500,
}

callbacks = {
    "modelcheckpoint":{
        "period":-1,
    },
    "guessingentropy":{
        "ge_rate":10,
        "n_repeat":25,
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
    return {'nonce':traceset["nonce"][index], 
            'k':traceset["key"][index],
            'subkey':subkey}

def get_known_key(traceset, subkey, index):
    return xoodyak.select_subkey(subkey, traceset['key'][index])

def intermediate_value(keyguess, trace_parameters):
    """Return the intermediate value of a key in the SBox . 
    nonce0 and nonce1 should be byte arrays of size (8) as they both are half of the nonce length (16 bytes).
    k should be a 2-bit value as an integer. This bit corresponds to the part of the key concerned in the attack given subkey.

    :param trace_parameters: Dictionary containing the trace parameters for intermediate value computation
    :type trace_parameters: dict
    :return: Intermediate value
    :rtype: Any
    """        
    return xoodyak.intermediate_value(keyguess,trace_parameters)