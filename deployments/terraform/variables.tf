variable "mysql_user" {}
variable "mysql_database" {}
variable "mysql_password" {}

variable "deployment_environment" {
  default = "dev"
}

variable "dns_endpoint_academy" {
  type = "map"

  default = {
    dev  = "dev.academy.fuchicorp.com"
    qa   = "qa.academy.fuchicorp.com"
    prod = "academy.fuchicorp.com"
  }
}

variable "mysql_host" {
  default = "academy-mysql-service"
}

variable "academy_service_account" {
  default = "fuchicorp-api"
}

variable "deployment_image" {
  default = "docker.fuchicorp.com/academy-dev:0.3"
}

variable "lets_encrypt_email" {
  default = "fuchicorpsolutions@gmail.com"
}

variable "academy_secret" {
  default = "WELCOME2019"
}
