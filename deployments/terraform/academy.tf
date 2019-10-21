data "template_file" "academy_values" {
  template = "${file("./academy/values_template.yaml")}"

  vars = {
    deployment_endpoint = "${lookup(var.dns_endpoint_academy, "${var.deployment_environment}")}"
    deployment_image    = "${var.deployment_image}"
    deployment_image    = "${var.deployment_image}"
    mysql_password      = "${var.mysql_password}"
    mysql_user          = "${var.mysql_user}"
    mysql_database      = "${var.mysql_database}"
    service_account     = "${var.academy_service_account}"
  }
}

resource "local_file" "academy_values_local_file" {
  content  = "${trimspace(data.template_file.academy_values.rendered)}"
  filename = "./academy/.cache/values.yaml"
}

resource "helm_release" "academy" {
  name      = "academy"
  namespace = "${var.deployment_environment}"
  chart     = "./academy"

  values = [
    "${data.template_file.academy_values.rendered}",
  ]
}