resource "kubernetes_secret" "academy_credentials" {
   "metadata" {
       name = "academy-credentials"
       namespace = "${var.deployment_environment}"
   }

   data {
       name = "mysql_user"
       value = "${var.mysql_user}"

       name = "mysql_database"
       value = "${var.mysql_database}"

       name = "mysql_password"
       value = "${var.mysql_password}"

       name = "admin_user"
       value = "${var.admin_user}"

       name = "admin_password"
       value = "${var.admin_password}"

       name = "mysql_root_password"
       value = "${var.mysql_root_password}"

       name = "github_token"
       value = "${var.github_token}"

       name = "github_client_id"
       value = "${var.github_client_id}"

       name = "github_client_secret"
       value = "${var.github_client_secret}"

       name = "application_secret"
       value = "${var.application_secret}"
         
   }
}
   	
	