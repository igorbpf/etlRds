#!/bin/bash

aws ec2 create-vpc-endpoint  --vpc-id vpc-c2f732a4 \
                             --vpc-endpoint-type Interface \
                             --service-name com.amazonaws.us-east-1.secretsmanager \
                             --subnet-ids=subnet-e6b334cb,subnet-a37f38c6,subnet-a47a0ced,subnet-e0f12adc,subnet-e841c0e4,subnet-818139da\
                             --security-group-id sg-06dc0a23e609e32ca
