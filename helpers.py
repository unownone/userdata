from bson.objectid import ObjectId
#helper function to convert object id
def  objidconv(inp):
    dic={}
    for keys,values in inp.items():
        if (keys!="_id" and keys!="password" and keys!="id"):
            dic[keys]=values
    return dic