variable "aws_region" {
  type    = string
  default = "us-west-1"
}

variable "project_name" {
  type    = string
  default = "ops-dashboard"
}

variable "origin_verify_secret" {
  type        = string
  description = "Secret header value CloudFront sends to ALB — rejects any request without it"
}
