#! bin/bash

mkdir build
mkdir build/logs

cp server.py build/.
cp logger.py build/.

echo "FROM python" >> build/Dockerfile
echo "RUN pip install flask" >> build/Dockerfile
echo "COPY  ./logs /home/IPAPP/logs/" >> build/Dockerfile
# echo "COPY  ./templates /home/IPAPP/templates/" >> build/Dockerfile
echo "COPY server.py /home/IPAPP/" >> build/Dockerfile
echo "COPY logger.py /home/IPAPP/" >> build/Dockerfile
echo "EXPOSE 5500" >> build/Dockerfile
echo "CMD python3 /home/IPAPP/server.py" >> build/Dockerfile

cd build
docker build -t ipApp .
docker run -t -d -p 5500:5500 --name apprunning ipApp
docker ps -a