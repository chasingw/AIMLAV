date > time.txt; python ./pytorch/train.py train --config_path=./configs/nuscenes/60_epochs/pedestrian-test.fhd.config --model_dir=model_ped_60_epochs --measure_time=True --resume=True; date >> time.txt; mv time.txt model_ped_60_epochs;

date > time.txt; python ./pytorch/train.py train --config_path=./configs/nuscenes/60_epochs/car-test.fhd.config --model_dir=model_car_60_epochs --measure_time=True; date >> time.txt; mv time.txt model_car_60_epochs;

date > time.txt; python ./pytorch/train.py train --config_path=./configs/nuscenes/60_epochs/barrier-test.fhd.config --model_dir=model_barrier_60_epochs --measure_time=True; date >> time.txt; mv time.txt model_barrier_60_epochs
