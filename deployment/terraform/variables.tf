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

variable "api_endpoint_platform" {
  type = "map"

  default = {
    dev  = "dev.api.academy.fuchicorp.com"
    qa   = "qa.api.academy.fuchicorp.com"
    prod = "api.academy.fuchicorp.com"
  }
}

variable "webplatform_service_account" {
  default = "fuchicorp-api"
}

variable "webplatform_image" {
  default = "docker.fuchicorp.com/webplatform-dev:0.2"
}

variable "api_platform_image" {
  default = "docker.fuchicorp.com/api-platform-dev"
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
