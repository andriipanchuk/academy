module "academy-deploy" {
  source  = "fuchicorp/chart/helm"

  deployment_name        = "academy-platform"
  deployment_environment = "${var.deployment_environment}"
  deployment_endpoint    = "${lookup(var.deployment_endpoint, "${var.deployment_environment}")}"
  deployment_path        = "academy-platform"

  template_custom_vars  = {
    mysql_password       = "${var.mysql_password}"
    mysql_root_password  = "${var.mysql_root_password}"
    mysql_user           = "${var.mysql_user}"
    mysql_database       = "${var.mysql_database}"
    deployment_image    = "${var.deployment_image}"
    ADMIN_USER           = "${var.ADMIN_USER}"
    ADMIN_PASSWORD       = "${var.ADMIN_PASSWORD}"
    service_account      = "${var.academy_service_account}"
    application_url      = "${lookup(var.deployment_endpoint, "${var.deployment_environment}")}"
    github_token         = "${var.github_token}"
    github_client_id     = "${lookup(var.github_client_id, "${var.deployment_environment}")}"
    github_client_secret = "${lookup(var.github_client_secret, "${var.deployment_environment}")}"
    application_secret   = "${var.application_secret}"
  }
}


