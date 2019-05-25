variable "mysql_user" {}
variable "mysql_database" {}
variable "mysql_host" {}
variable "webplatform_namespace" {}
variable "environment" {
  default = "dev"
}

variable "issuer_name" {
  type = "map"
  default = {
    dev  = "letsencrypt-issuer-dev-webplatform-prod"
    qa   = "letsencrypt-issuer-qa-webplatform-prod"
    prod = "letsencrypt-issuer-prod-webplatform-prod"
  }
}

variable "bucket_name" {
  type = "map"
  default = {
    dev  = "webplatform_dev"
    qa   = "webplatform_qa"
    prod = "webplatform_prod"
  }
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
