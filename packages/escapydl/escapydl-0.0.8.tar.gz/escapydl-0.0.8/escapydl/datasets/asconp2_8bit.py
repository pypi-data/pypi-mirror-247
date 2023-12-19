import os
import torch
import helpers.ascon_helper as ascon
import Utils

sbox_chunk_size = 8
parameters = {
    "dataset_name"        : "data/ASCON_P2_CPA_all_mlpsca_ready.trs",
    "dataset_size"        : 510000,
    "training_size"       : 500000,
    "val_size"            : 10000,
    "subkey"              : 0,
    "num_key_hypotheses"  : 2**(sbox_chunk_size),
    "n_samples"           : 1408,
    "r"                   : 0.8,
    "n_repeat"            : 50,
    "ge_rate"             : 5,
    "shuffle"             : True,
    "chunk_size"          : sbox_chunk_size,
}

model = {
    "num_epochs"          : 500,
    "loss_function"       : Utils.FocalLoss(),
    "lr"                  : 1e-03,
    "bs"                  : 512,
}

callbacks = {
    "modelcheckpoint":{
        "period":-1,
    },
    "guessingentropy":{
        "ge_rate":5,
        "n_repeat":5,
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
    return ascon.select_subkey_sbox_chunk(subkey, traceset['key'][index], chunk_size=parameters["chunk_size"])

def intermediate_value(keyguess, trace_parameters):
    """Return the intermediate value of a key in the SBox . 
    nonce0 and nonce1 should be byte arrays of size (8) as they both are half of the nonce length (16 bytes).
    k should be a 3-bit value as an integer. This bit corresponds to the part of the key concerned in the attack given subkey.

    :param trace_parameters: Dictionary containing the trace parameters for intermediate value computation
    :type trace_parameters: dict
    :return: Intermediate value
    :rtype: Any
    """        
    return ascon.intermediate_value_sbox_chunk(keyguess,trace_parameters, chunk_size=parameters["chunk_size"])