abshpath=$(dirname "$(realpath "$0")")
cd "$abshpath" || exit

python3 main.py &
python3 box.py &
python3 "${abshpath}/estimate.py" &

wait