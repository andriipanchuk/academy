resource "kubernetes_secret" "academy_credentials" {
   "metadata" {
       name = "academy-credentials"
       namespace = "${var.deployment_environment}"
   }

   data {
       
       mysql_user = "${var.mysql_user}"

       
       mysql_database = "${var.mysql_database}"

      
       mysql_password = "${var.mysql_password}"

       
       admin_user = "${var.admin_user}"

       
       admin_password = "${var.admin_password}"

       
       mysql_root_password = "${var.mysql_root_password}"

       
       github_token = "${var.github_token}"

       
       github_client_id = "${lookup(var.github_client_id, "${var.deployment_environment}")}"


       github_client_secret = "${lookup(var.github_client_secret, "${var.deployment_environment}")}"

       
       application_secret = "${var.application_secret}"

       vimeo_client_secret = "${var.vimeo_client_secret}"

       vimeo_access_token = "${var.vimeo_access_token}"

       vimeo_client_id = "${var.vimeo_client_id}"


         
   }
}
   	
	