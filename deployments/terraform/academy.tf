data "template_file" "academy_values" {
  template = "${file("./academy/values_template.yaml")}"

  vars = {
    deployment_endpoint  = "${lookup(var.dns_endpoint_academy, "${var.deployment_environment}")}"
    deployment_image     = "${var.deployment_image}"
    deployment_image     = "${var.deployment_image}"
    mysql_password       = "${var.mysql_password}"
    mysql_user           = "${var.mysql_user}"
    mysql_database       = "${var.mysql_database}"
    service_account      = "${var.academy_service_account}"
    application_url      = "${lookup(var.dns_endpoint_academy, "${var.deployment_environment}")}"
    github_token         = "${var.github_token}"
    github_client_id     = "${lookup(var.github_client_id, "${var.deployment_environment}")}"
    github_client_secret = "${lookup(var.github_client_secret, "${var.deployment_environment}")}"
    application_secret   = "${var.application_secret}"
  }
}

resource "local_file" "academy_values_local_file" {
  content  = "${trimspace(data.template_file.academy_values.rendered)}"
  filename = "./academy/.cache/values.yaml"
}

resource "helm_release" "academy" {
  name      = "academy-${var.deployment_environment}"
  namespace = "${var.deployment_environment}"
  chart     = "./academy"

  values = [
    "${data.template_file.academy_values.rendered}",
  ]
}
