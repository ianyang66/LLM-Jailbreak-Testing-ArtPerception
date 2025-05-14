export CUDA_VISIBLE_DEVICES=0,1
# nohup python3 reg_test_only.py --model llama3-8b --direction h --ps ict-no-no --num 50 --length 4,6,8,10  --dir ./ict_result

nohup python3 reg_test_only.py --model llama3-8b --direction h --ps ict-no-no --num 50 --length 4,6,8,10  --dir ./ict_result --ict_size 4
