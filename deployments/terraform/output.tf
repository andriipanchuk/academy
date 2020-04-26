output "application_deployed" {
  value = "${lookup(var.deployment_endpoint, "${var.deployment_environment}")}"
}