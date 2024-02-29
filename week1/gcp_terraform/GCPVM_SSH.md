# GCP VM and SSH

## Generate and setting ssh key in ~/.ssh
```
ssh-keygen -t rsa -f gcp -C mazaya -b 2048
```
1) open VM, Settings, Metadata, SSH Keys, add using gcp.pub
2) VM Create Instances, use e2 standard 4CPU 16GB Mem, 30 GB Ubuntu 20.04 disk
3) Install Anaconda
```
ssh -i ~/.ssh/gcp mazaya@${external IP}
gcloud --version
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
bash Anaconda3-2021.11-Linux-x86_64.sh
```
4) Make a config file inside ~/.ssh, upon installation of anaconda, it will be written in .bashrc
```
ssh de-zoomcamp # login
logout
source .bashrc  # use base
```
## Docker + compose
```
sudo apt-get update
sudo apt-get install docker.io
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart         # login and logout
docker run hello-world
docker run -it ubuntu bash
```
### Setting docker compose
```
wget https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -O docker-compose
chmod +x docker-compose
./docker-compose version
nano .bashrc
    export PATH="${HOME}/bin:${PATH}"
source .bashrc
docker-compose version
```
**git clone de-zoomcamp github, move to docker_sql to docker-compose.yaml file**
```
docker-compose up -d
docker ps
pip install pgcli       # diff terminal
sudo apt install python3-psycopg2
pgcli -h localhost -U root -d ny_taxi
```
## Other tools
### pgcli and pgadmin
1) open terminal and forward port 5432 and 8080
2) http://localhost:8080 shud work (admin@admin.com)

### jupyter notebook
1) use upload-data.ipynb
```
jupyter notebook
```
2) forward port 8888, copy pase URL to the browser
3) download dataset
```
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
gzip -d yellow_tripdata_2021-01.csv.gz
```
4) run notebook, i had to install cond psycopg2 first
```
pgcli -h localhost -U root -d ny_taxi
\dt
select count(1) from yellow_taxi_data
```

### terraform
```
wget https://releases.hashicorp.com/terraform/1.1.3/terraform_1.1.3_linux_amd64.zip
unzip terraform_1.1.3_linux_amd64.zip           # in /bin
terraform --version
```
1) Cd to terraform in dezoomcamp directory
2) Refer to Basic Terraform.md and create key in json to connect
3) sftp google credentials to VM, in local terminal run
```
sftp de-zoomcamp
mkdir and cd .gc
put ny-rides.json
export GOOGLE_CREDENTIALS=~/.gc/my-rides.json
gcloud auth activate-service-account --key-file $GOOGLE_CREDENTIALS
```
```
terraform init
terraform plan
terraform apply
```

## Shut down, restart, and delete VM
1) can go to GCP VM Instances, Stop
```
sudo shutdown now
```
2) can go to GCP VM Instances, Start
3) copy and replace external IP to config
```
nano .ssh/config
ssh de-zoomcamp
sudo shutdown now
```
4) delete VM can go to GCP VM Instances, Delete
