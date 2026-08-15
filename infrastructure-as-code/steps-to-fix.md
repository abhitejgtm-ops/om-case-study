# Steps to fix

1. Change the Terraform resource from `count` to `for_each` so that each resource has a stable key.

2. Define stable keys for all five resources:
   - `resource_0`
   - `resource_1`
   - `resource_2`
   - `resource_3`
   - `resource_4`

3. The resources will then be addressed as:
   - `resource.example["resource_0"]`
   - `resource.example["resource_1"]`
   - `resource.example["resource_2"]`
   - `resource.example["resource_3"]`
   - `resource.example["resource_4"]`

4. Remove only the `resource_1` key from the `for_each` map.

5. Run `terraform plan` and verify that only `resource.example["resource_1"]` will be destroyed.

6. Confirm that `resource.example["resource_0"]`, `resource.example["resource_2"]`, `resource.example["resource_3"]`, and `resource.example["resource_4"]` have no changes.

7. Run `terraform apply` after reviewing the plan to delete only the second resource without affecting the others.
