
import numpy as np
import os, time
from transformers import AutoTokenizer

import onnxruntime
from onnxruntime import InferenceSession, SessionOptions
from onnxruntime.capi.onnxruntime_pybind11_state import InvalidArgument

FLAG_SOFTMAX_USE = False
def softmax(logits):
    logits = np.exp(logits)
    s = sum(logits)
    for i in range(3):
        logits[i]=logits[i]/s
    return logits

news_list = ["How the GBTC premium commerce ruined Barry Silbert, his DCG empire and took crypto lending platforms with them",
             "MicroStrategy’s Bitcoin Strategy Sets Tongues Wagging Even As It Doubles Down On BTC Purchases ⋆ ZyCrypto",
             "How the GBTC premium trade ruined Barry Silbert, his DCG empire and took crypto lending platforms with them",
             "Bitcoin Holders To Expect More Difficulties As Data Point To Looming BTC Price Drop",
             "Bitcoin Breaks Past $17,000 Barrier – Will BTC Also Breach 4% Weekly Run?",
             "Bitcoin Price Today 9 Jan: BTC Increases By 1.79% Painting The Chart Green",
             "Bitcoin: This is what large investor and retail interest can do for BTC over time"
]
model_name = "ElKulako/cryptobert"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast = False)
options = SessionOptions()
options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
options.intra_op_num_threads = 1
session = InferenceSession("bert.onnx", options, providers=["CPUExecutionProvider"])
session.disable_fallback()
t_start = time.time()
onnx_output = []
for n in news_list:
    inputs = tokenizer(n)
    input_feed = {"input_ids": np.array(inputs["input_ids"]).reshape(1, -1)}
    try:
        output = session.run(
            output_names=["output"],
            input_feed=input_feed
        )[0][0]
        if FLAG_SOFTMAX_USE:
            output = softmax(output)
        onnx_output.append(output)
    except (RuntimeError, InvalidArgument) as e:
        print(e)

        # str ="{:.6f}, {:.6f}, {:.6f}".format(output[0], output[1], output[2])) after softmax
t_onnx = time.time() - t_start
print("{} новостей обработано за {}c {}".format(len(news_list), t_onnx,
                                                ("с softmax" if FLAG_SOFTMAX_USE else "без softmax")))

