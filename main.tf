resource "null_resource" "execbluecat"{
  provisioner "local-exec"{
    command = "pwd && ls -la 1>&2; exit 125"
    #command = "python3 main.py --hostname \"${var.hostname}\" --value \"${var.value}\" --svcPassword \"${var.password}\""
  }
}
