from common.funs import getfromstore, addtostore

#load documents into store
store2 = addtostore(folder_name="sou",collection_name="sou_coll",persist_directory="db/")
print(store2.get(["metadatas"]))