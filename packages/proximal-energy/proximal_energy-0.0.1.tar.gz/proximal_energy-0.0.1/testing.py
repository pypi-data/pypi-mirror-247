import pprint

import proximal_energy

pp = pprint.PrettyPrinter(indent=4)

client = proximal_energy.ProximalClient("insert_api_key_here")

try:
    projects = client.get_projects()

    if projects.status_code == 200:
        print("Successfully retrieved projects!")
        pp.pprint(projects.json())
    else:
        print(
            "Failed to retrieve projects. Status code: {}".format(projects.status_code)
        )
except Exception as e:
    print("Ran into an error, bummer...")
    print(e)
