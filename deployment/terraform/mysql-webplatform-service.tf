resource "kubernetes_service" "${var.mysql_host}" {
  metadata {
    name = "${var.mysql_host}"
    namespace = "${var.webplatform_namespace}"
  }
  spec {
    clusterIP = "null"
    selector { run = "webplatform-mysql"  }
    port {
      port = 3306
      target_port = 3306
    }

    type = "ClusterIP"
  }
}
