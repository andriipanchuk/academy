resource "helm_release" "webplatform_services_ingress" {

  name = "webplatform-services-ingress-${var.webplatform_namespace}"
  namespace = "${var.webplatform_namespace}"
  chart = "./helm-deployment"

  set {
    name = "dns_endpoint"
    value = "${lookup(var.dns_endpoint_webplatform, "${var.environment}")}"
  }

  set {
    name = "webplatform_service"
    value = "${kubernetes_service.webplatform_service.metadata.0.name}"
  }

  set {
    name = "webplatform_port"
    value = "${kubernetes_service.webplatform_service.spec.0.port.0.port}"
  }

  set {
    name = "api_endpoint"
    value = "${lookup(var.api_endpoint_platform, "${var.environment}")}"
  }

  set {
    name = "api_platform_service"
    value = "${kubernetes_service.api_platform_service.metadata.0.name}"
  }

  set {
    name = "api_platform_port"
    value = "${kubernetes_service.api_platform_service.spec.0.port.0.port}"
  }

  set {
    name = "email"
    value = "${var.lets_encrypt_email}"
  }

}
