resource "null_resource" "execbluecat"{
  provisioner "local-exec"{
    command = "pwd && ls -la > /tmp/out.txt"
    #command = "python3 main.py --hostname \"${var.hostname}\" --value \"${var.value}\" --svcPassword \"${var.password}\""
  }
}
