resource "kubernetes_service" "api_platform_service" {

  metadata {
    name = "api-platform-service"
    namespace = "${var.webplatform_namespace}"
  }

  spec {
    selector { run = "api-platform"  }

    port {
      port = 7102
      target_port = 5000
    }

    type = "NodePort"
  }
}
