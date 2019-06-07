variable "mysql_user" {}
variable "mysql_database" {}
variable "mysql_host" {}
variable "webplatform_namespace" {}

variable "environment" {
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

variable "webplatform_service_account" {
  default = "fuchicorp-api"
}

variable "webplatform_image" {
  default = "docker.fuchicorp.com/webplatform-dev:0.2"
}

variable "lets_encrypt_email" {
  default = "fuchicorpsolutions@gmail.com"
}

variable "webplatform_password" {
  default = "Welcome2019"
}

variable "webplatform_secret" {
  default = "WELCOME2019"
}
