resource "helm_release" "webplatform_services_ingress" {

  name = "webplatform-services-ingress-${var.webplatform_namespace}"
  namespace = "${var.webplatform_namespace}"
  chart = "./helm-deployment"


  set {
    name = "dns_endpoint"
    value = "${var.dns_endpoint_webplatform}"
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
    name = "email"
    value = "${var.lets_encrypt_email}"
  }

}
