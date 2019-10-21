output "selected_github_client_id" {
  value = "${lookup(var.github_client_id, "${var.deployment_environment}")}"
}

output "selected_github_client_secret" {
  value = "${lookup(var.github_client_secret, "${var.deployment_environment}")}"
}

output "application_deployed" {
  value = "${lookup(var.dns_endpoint_academy, "${var.deployment_environment}")}"
}
