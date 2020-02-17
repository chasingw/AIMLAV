date > time.txt; python ./pytorch/train.py evaluate --config_path=./configs/nuscenes/20_epochs/pedestrian-test.fhd.config --model_dir=model_ped_20_epochs --measure_time=True; date >> time.txt; mv time.txt model_ped_20_epochs;

date > time.txt; python ./pytorch/train.py evaluate --config_path=./configs/nuscenes/20_epochs/barrier-test.fhd.config --model_dir=model_barrier_20_epochs --measure_time=True; date >> time.txt; mv time.txt model_barrier_20_epochs

date > time.txt; python ./pytorch/train.py evaluate --config_path=./configs/nuscenes/20_epochs/car-test.fhd.config --model_dir=model_car_20_epochs --measure_time=True; date >> time.txt; mv time.txt model_car_20_epochs
