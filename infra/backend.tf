terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 6.0.0"
    }
  }  

  backend "s3" {
    bucket       = "kevin-terraform-state"
    key          = "container-microservices/terraform.tfstate"
    region       = "us-west-1"
    use_lockfile = true
    encrypt      = true
  }
}

