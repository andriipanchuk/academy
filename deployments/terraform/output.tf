output "selected_github_client_id" {
  value = "${lookup(var.github_client_id, "${var.deployment_environment}")}"
}

output "selected_github_client_secret" {
  value = "${lookup(var.github_client_secret, "${var.deployment_environment}")}"
}

output "application_deployed" {
  value = "${lookup(var.deployment_endpoint, "${var.deployment_environment}")}"
}

output "admin_user" {
  value = "${var.admin_user}"
}
output "admin_password" {
  value = "${var.admin_password}"
}
