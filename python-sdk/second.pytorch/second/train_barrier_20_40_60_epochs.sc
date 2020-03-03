date > time.txt; python ./pytorch/train.py train --config_path=./configs/nuscenes/40_epochs/barrier-test.fhd.config --model_dir=model_barrier_40_epochs --measure_time=True; date >> time.txt; mv time.txt model_barrier_40_epochs;

date > time.txt; python ./pytorch/train.py train --config_path=./configs/nuscenes/60_epochs/barrier-test.fhd.config --model_dir=model_barrier_60_epochs --measure_time=True; date >> time.txt; mv time.txt model_barrier_60_epochs;

date > time.txt; python ./pytorch/train.py train --config_path=./configs/nuscenes/20_epochs/barrier-test.fhd.config --model_dir=model_barrier_20_epochs --measure_time=True; date >> time.txt; mv time.txt model_barrier_20_epochs
