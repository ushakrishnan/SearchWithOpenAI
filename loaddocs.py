from common.funs import addtostorepdf, addtostoretxt, getfromstore

#load documents into store
store2 = addtostorepdf(folder_name="sou",collection_name="sou_coll",persist_directory="db/")
print(store2.get(["metadatas"]))

store2 = addtostoretxt(folder_name="sou",collection_name="sou_coll",persist_directory="db/")
print(store2.get(["metadatas"]))

#get document store
store = getfromstore(collection_name="sou_coll")
print(store.get(["metadatas"]))