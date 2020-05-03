module "academy-deploy" {
  source  = "fuchicorp/chart/helm"

  deployment_name        = "academy-platform"
  deployment_environment = "${var.deployment_environment}"
  deployment_endpoint    = "${lookup(var.deployment_endpoint, "${var.deployment_environment}")}"
  deployment_path        = "academy"

  template_custom_vars  = {     
    deployment_image     = "${var.deployment_image}"    
    service_account      = "${var.academy_service_account}"    
    academy_credentials  = "${kubernetes_secret.academy_credentials.metadata.0.name}"
  }
}