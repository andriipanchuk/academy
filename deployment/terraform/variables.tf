variable "mysql_user" {}
variable "mysql_database" {}
variable "mysql_password" {}
variable "deployment_namespace" {}

variable "deployment_environment" {
  default = "dev"
}

variable "dns_endpoint_webplatform" {
  type = "map"

  default = {
    dev  = "dev.academy.fuchicorp.com"
    qa   = "qa.academy.fuchicorp.com"
    prod = "academy.fuchicorp.com"
  }
}

variable "mysql_host" {
  default = "webplatform-mysql-service"
}

variable "webplatform_service_account" {
  default = "fuchicorp-api"
}

variable "webplatform_image" {
  default = "docker.fuchicorp.com/webplatform-dev:0.2"
}

variable "lets_encrypt_email" {
  default = "fuchicorpsolutions@gmail.com"
}


variable "webplatform_secret" {
  default = "WELCOME2019"
}
