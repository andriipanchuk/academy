module "academy-deploy" {
  source = "fuchicorp/chart/helm"

  deployment_name        = "academy-platform"
  deployment_environment = "${var.deployment_environment}"
  deployment_endpoint    = "${lookup(var.deployment_endpoint, "${var.deployment_environment}")}"
  deployment_path        = "academy"

  template_custom_vars = {
    mysql_password       = "${var.mysql_password}"
    mysql_root_password  = "${var.mysql_root_password}"
    mysql_user           = "${var.mysql_user}"
    mysql_database       = "${var.mysql_database}"
    deployment_image     = "${var.deployment_image}"
    admin_user           = "${var.admin_user}"
    admin_password       = "${var.admin_password}"
    service_account      = "${var.academy_service_account}"
    application_url      = "${lookup(var.deployment_endpoint, "${var.deployment_environment}")}"
    github_token         = "${var.github_token}"
    github_client_id     = "${lookup(var.github_client_id, "${var.deployment_environment}")}"
    github_client_secret = "${lookup(var.github_client_secret, "${var.deployment_environment}")}"
    application_secret   = "${var.application_secret}"
    vimeo_client_id      = "${var.vimeo_client_id}"
    vimeo_client_secret  = "${var.vimeo_client_secret}"
    vimeo_access_token   = "${var.vimeo_access_token}"
  }
}
