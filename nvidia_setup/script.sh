git clone https://github.com/DjoserKhemSimeu/inference_results_v1.1.git
/grid5000/code/bin/g5k-setup-nvidia-docker -t
mkdir scratch
export MLPERF_SCRATCH_PATH=/tmp/scratch/
mkdir $MLPERF_SCRATCH_PATH/data $MLPERF_SCRATCH_PATH/models $MLPERF_SCRATCH_PATH/preprocessed_data
cd inference_results_v1.1/closed/NVIDIA/
#front end :
scp -r NVIDIA/docker/ root@abacus10-1.rennes.grid5000.fr:/tmp/inference_results_v1.1/closed/NVIDIA/docker/
#uname -p -> uname -m Makefile
make prebuild
echo $MLPERF_SCRATCH_PATH
ls -al $MLPERF_SCRATCH_PATH
make clean
make link_dirs
ls -al build/
make download_data BENCHMARKS="bert"
make download_model BENCHMARKS="bert"
make preprocess_data BENCHMARKS="bert"
export CUDA_VISIBLE_DEVICES=0
pip install setuptools==70.0.0
make build
# add :
# CUDA_VISIBLE_ORDER=PCI_BUS_ID nvidia-smi --query-gpu=gpu_name,pci.device_id --format=csv
# in closed/NVIDIA/code/common/system_list.py :
# RTX_2080_Ti =SystemClass("GeForce RTX 2080 Ti", ["GeForce RTX 2080 Ti"], ["1E04"], Architecture.Turing, [1, 4])
# in closed/NVIDIA/config/bert/Offline/__init__.py:
# @ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
#class RTX_2080_Tix4(OfflineGPUBaseConfig):
#    system = System("GeForce RTX 2080 Ti", Architecture.Turing, 4)
#    enable_interleaved = True
#    use_small_tile_gemm_plugin = False
#    gpu_batch_size = 8
#    gpu_copy_streams = 1
#    gpu_inference_streams = 1
#    offline_expected_qps = 97
make run RUN_ARGS="--benchmarks=bert --scenarios=offline"
# This version of MLPerf (TensorRT 8.0.1) support only Xavier;, Turing and Ampere GPU arch, if we want to add Ada GPU arch we must pass to 8.5.1
