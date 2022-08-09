#!/bin/bash

# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/optimize_gpu.html
sudo nvidia-persistenced
sudo nvidia-smi -ac 5001,1590
