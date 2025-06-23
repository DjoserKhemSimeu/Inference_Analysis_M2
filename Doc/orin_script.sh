#cd
sudo apt update
sudo apt install python3-pip
sudo pip3 install -U jetson-stats
#reboot
sudo apt install nvidia-jetpack
sudo apt install docker.io
sudo systemctl start docker
sudo apt install curl
sudo apt install docker-buildx
#cd /tmp
git clone https://github.com/DjoserKhemSimeu/inference_results_v4.1.git
mkdir scratch
export MLPERF_SCRATCH_PATH=/tmp/scratch/
mkdir $MLPERF_SCRATCH_PATH/data $MLPERF_SCRATCH_PATH/models $MLPERF_SCRATCH_PATH/preprocessed_data
cd inference_results_v4.1/closed/NVIDIA/
make prebuild DOCKER_ARGS="--security-opt systempaths=unconfined"
#python3 -m scripts.custom_systems.add_custom_system
echo $MLPERF_SCRATCH_PATH
ls -al $MLPERF_SCRATCH_PATH
make clean
make link_dirs
ls -al build/
make download_data BENCHMARKS="bert"
make download_model BENCHMARKS="bert"
make preprocess_data BENCHMARKS="bert"
make build
make run RUN_ARGS="--benchmarks=bert --scenarios=singlestream"
