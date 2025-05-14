export CUDA_VISIBLE_DEVICES=6,7

nohup python3 main.py --direction v --ps sep-head-no --mType word --model gemma2-9b --dir ./results  --top_n 1 --font cards 
