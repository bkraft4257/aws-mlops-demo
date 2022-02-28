#!/bin/bash

# Install Docker 
# https://www.cyberciti.biz/faq/how-to-install-docker-on-amazon-linux-2/

export USER=ec2-user
export AIRFLOW_PATH=/home/ec2-user/airflow

yum update -y
yum install docker vim git -y

groupadd docker
usermod -aG docker ${USER}

systemctl enable docker
systemctl start docker


# Install Docker Compose
# https://docs.docker.com/compose/install/

 curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
 chmod +x /usr/local/bin/docker-compose

# install awscli v2, according to https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-install
zip_file="awscliv2.zip"
cd /tmp
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o $zip_file
unzip $zip_file
./aws/install
rm $zip_file
rm -rf ./aws
cd -  # Return to previous directory

# Install Airflow
# https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html


mkdir -p $AIRFLOW_PATH
cd $AIRFLOW_PATH

mkdir -p ./dags ./logs ./plugins

echo -e "AIRFLOW_GID=0" > .env
echo -e "AIRFLOW_UID=$(id -u)" >> .env
echo -e "_AIRFLOW_WWW_USER_USERNAME=admin_phdata" >> .env
echo -e "_AIRFLOW_WWW_USER_PASSWORD=adambrockmac" >> .env 

echo -e "#!/bin/bash" > airflow_start.sh
echo -e "docker-compose up airflow-init" >> airflow_start.sh
echo -e "docker-compose up" >> airflow_start.sh
chmod +x airflow_start.sh

# Download docker compose file for Airflow
# I am unable to find a docker-compose.yaml file for Airflow 1.10.15. 

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.3/docker-compose.yaml'

cd /home/${USER}
chown -R ${USER}:${USER} airflow

reboot
