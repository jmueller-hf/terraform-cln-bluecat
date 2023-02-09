resource "null_resource" "execbluecat"{
  provisioner "local-exec"{
    command = "python main.py --hostname \"${var.hostname}\" --value \"${var.value}\" --svcPassword \"${var.password}\""
  }
}
