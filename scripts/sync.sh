
rsync -Pav \
--delete \
--exclude-from .rsyncignore \
-e "ssh -i peanuts4.pem" \
. \
ubuntu@ec2-35-178-162-251.eu-west-2.compute.amazonaws.com:/home/ubuntu/thor
