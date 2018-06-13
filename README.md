# RushCafe Project


## CMS

The CMS is written with Django, utilizing the standard Django authentication backend.

### Testing

`coverage run --source='.' manage.py test rushcafe`

## Deployment

The web application is being hosting on an EC2 server using `docker-machine` and `docker-compose`.

Environment files with production ENV variables are not included in this repository.

### Create EC2 Instance with Docker

`docker-machine create --driver amazonec2 --amazonec2-region ap-southeast-2 rushcafe`

### Initialize Environment and then Deploy with Compose

`eval $(docker-machine env rushcafe)`

`docker-compose build`

`docker-compose up -d`

### Copy to Volume and Collect Static Files

We could build the Docker image with the files inside instead, which is what I would do for a production build normally.

`docker-machine scp -r web rushcafe:/home/ubuntu/`

`docker-compose exec web bash`

`python manage.py collectstatic`