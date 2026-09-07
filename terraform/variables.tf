variable "aws_region" {
  description = "AWS region — must match where your key pair 'devops-lab-key' exists"
  type        = string
}

variable "key_name" {
  description = "Existing EC2 key pair name"
  type        = string
  default     = "devops-lab-key"
}

variable "my_ip" {
  description = "Your public IP in CIDR form, e.g. 103.45.67.89/32"
  type        = string
}
