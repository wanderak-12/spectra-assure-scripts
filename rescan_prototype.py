import os
from spectra_assure_api_client import SpectraAssureApiOperations

api = SpectraAssureApiOperations (
    server = os.getenv("RLPORTAL_SERVER"),
    organization = os.getenv("RLPORTAL_ORG"),
    group = os.getenv("RLPORTAL_GROUP"),
    token = os.getenv("RLPORTAL_ACCESS_TOKEN") 
    )

print(f"Success! Connected to Spectra Assure.")
print(f"Group: {api.group}")

# input: project and package names
project_name = input("Enter Project Name: ")
package_name = input("Enter Package Name: ")

# asks the portal for all info about this package
response = api.list(project = project_name, package = package_name)

# if the request worked status 200 shows up
if response.status_code == 200:
    # turns the response into a readable list
    data = response.json()

    # grabs just the 'versions' section
    version_list = data.get("versions", [])

    # checks if the package is empty or actually has versions to scan
    if not version_list:
        print(f"No versions found for package '{package_name}'.")
    else:
        # then tells the user how many versions we found before starting the loop
        print(f"Found {len(version_list)} versions. Starting rescan...")

        # looks at every version found in that list
        for v in version_list:
            version_name = v.get("version")

            # tells the portal to re-analyze/sync this specific version
            if version_name:
                rescan_response = api.sync(
                    project = project_name,
                    package = package_name,
                    version = version_name
                )
                # prints the result (200 means it's done, 202 means it started)
                print(f"Rescan called for version {version_name}: Status {rescan_response.status_code}")
else:
    print(f"Failed to list versions. Status: {response.status_code}")


