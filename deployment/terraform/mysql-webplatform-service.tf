resource "kubernetes_service" "mysql_host" {

  metadata {
    name = "${var.mysql_host}"
    namespace = "${var.deployment_namespace}"
  }
  spec {

    selector { run = "webplatform-mysql"  }
    port {
      port = 3306
      target_port = 3306
    }
  }
}
