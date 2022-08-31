#!/bin/bash

# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html
# Option 4: NVIDIA gaming drivers (G5 and G4dn instances)
sudo yum install -y kernel-devel-$(uname -r)
aws s3 cp --recursive s3://nvidia-gaming/linux/latest/ .
unzip *Gaming-Linux-Guest-Drivers.zip -d nvidia-drivers
chmod +x nvidia-drivers/NVIDIA-Linux-x86_64*-grid.run
sudo CC=/usr/bin/gcc10-cc ./nvidia-drivers/NVIDIA-Linux-x86_64*.run

cat << EOF | sudo tee -a /etc/nvidia/gridd.conf
vGamingMarketplace=2
EOF

sudo curl -o /etc/nvidia/GridSwCert.txt "https://nvidia-gaming.s3.amazonaws.com/GridSwCert-Archive/GridSwCertLinux_2021_10_2.cert"
sudo touch /etc/modprobe.d/nvidia.conf
echo "options nvidia NVreg_EnableGpuFirmware=0" | sudo tee --append /etc/modprobe.d/nvidia.conf

# Install CUDA Toolkit
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html#gpu-instance-install-cuda
# https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#runfile
sudo su ec2-user -c 'wget -O ~/cuda.run https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/cuda_11.7.1_515.65.01_linux.run'
sudo su ec2-user -c 'sudo sh ~/cuda.run --silent --toolkit --override --no-opengl-libs --no-man-page'
