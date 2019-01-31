# import yaml
# from itertools import chain
#
# with open("meta.yaml") as f:
#     list_doc = yaml.load(f)
#
# version = list_doc['package']['version']
# next_version = ''.join(list(version)[:-1] + [str(int(list(version).pop()) + 1)])
# list_doc['package']['version'] = next_version
#
# with open("meta.yaml", "w") as f:
#     yaml.dump(list_doc, f)
#
#
# def version():
#     with open("meta.yaml") as f:
#         list_doc = yaml.load(f)
#         version = list_doc['package']['version']
#     return version
