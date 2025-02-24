DOCKER_DEFAULT_PLATFORM="linux/amd64" docker build -t justextract .
aws lightsail push-container-image --region ap-southeast-1 --service-name justextract --label backend --image justextract:latest