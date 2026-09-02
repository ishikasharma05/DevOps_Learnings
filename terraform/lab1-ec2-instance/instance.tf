provider "aws" {
  region = "ap-south-1"
}
resource "aws_vpc" "may-2026-vpc-tf" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  enable_dns_support = true
  tags = {
    Name = "may-2026-vpc-tf"
  }
}
resource "aws_subnet" "may-2026-subnet-tf" {
  vpc_id     = aws_vpc.may-2026-vpc-tf.id
  cidr_block = "10.0.1.0/24"
  tags = {
    Name = "may-2026-subnet-tf"
  }
}

resource "aws_security_group" "may-2026-sg-tf" {
  vpc_id      = aws_vpc.may-2026-vpc-tf.id
  name        = "may-2026-sg-tf"
  description = "Security group for may-2026-ec2-tf"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["103.54.189.254/32"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "may-2026-ec2-tf" {
  ami           = "ami-01a00762f46d584a1"
  instance_type = "t3.micro"
  key_name      = "april-lab"
  count         = 1
  subnet_id     = aws_subnet.may-2026-subnet-tf.id
  vpc_security_group_ids = [
    aws_security_group.may-2026-sg-tf.id
  ]
  tags = {
    Name = "may-2026-ec2-tf"
  }
}
