DIRECTORY_NAME="plot-from-csv"
IMAGE_NAME="plot-from-csv-backend"

mkdir -p .build/$DIRECTORY_NAME/scripts
cd .build/$DIRECTORY_NAME

printf "version: '3'\
\n\
\nservices:\
\n  postgis:\
\n    container_name: backend\
\n    image: plot-from-csv-backend\
\n    restart: on-failure\
\n    ports:\
\n      - 8000:8000\
\n    env_file: .env\
\n"\
 | tee docker-compose.yml

printf "SERVER_HOST = 0.0.0.0\
\nSERVER_PORT = 8000 \
\nCACHE = '/plot-from-csv/backend/src/cache'\
\n"\
 | tee .env

printf " \n"
