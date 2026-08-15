variable "files" {
  default = 5
}

locals {
  file_names = {
    file0 = 0

    file2 = 2
    file3 = 3
    file4 = 4
  }
}

resource "local_file" "foo" {
  for_each = local.file_names

  content  = "# Some content for file ${each.value}"
  filename = "${each.key}.txt"
}
