from common.funs import getfromstore

#get document store
store = getfromstore(collection_name="sou_coll")
print(store.get(["metadatas"]))