# vllm-gpt-oss

This repo has the startup script and documentation for how i am hosting gpt-oss-120b with tool calling enabled, with vllm running on blackwell/cuda 12.9.

## Set up a the virtual directory

```
python  -m venv .venv
source .venv/bin/activate
export GPTOSS=$(pwd)
```

## Clone the vllm repo, compile and install it

```
git clone https://github.com/vllm-project/vllm.git
cd vllm
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu129
python use_existing_torch.py
python -m pip install -r requirements/build.txt
python -m pip install -r requirements/common.txt
install cuda toolkit: https://developer.nvidia.com/cuda-toolkit-archive
export MAX_JOBS=64
python -m pip install --no-build-isolation -v .
```

## install flash inference

```
cd $GPTOSS
git clone https://github.com/flashinfer-ai/flashinfer.git --recursive
cd flashinfer
pip install ninja # required for build system
export TORCH_CUDA_ARCH_LIST="12.0+PTX" # adjust if needed
python -m flashinfer.aot # precompile AOT kernels
pip install --no-build-isolation --verbose .
```

## install the hf cli and download the model

```
cd $GPTOSS
pip install --upgrade huggingface_hub[cli]
hf download openai/gpt-oss-120b
```

## review the startup script and change any variables needed for hosting or the api key, then launch the server

```
./run_gpt-oss-120b.py
```
